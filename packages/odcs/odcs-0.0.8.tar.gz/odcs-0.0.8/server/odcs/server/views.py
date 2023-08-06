# -*- coding: utf-8 -*-
# Copyright (c) 2017  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Jan Kaluza <jkaluza@redhat.com>

import datetime

from flask.views import MethodView
from flask import request, jsonify, g

from odcs.server import app, db, log, conf
from odcs.server.errors import NotFound, BadRequest
from odcs.server.models import Compose
from odcs.server.types import (
    COMPOSE_RESULTS, COMPOSE_FLAGS, COMPOSE_STATES, PUNGI_SOURCE_TYPE_NAMES)
from odcs.server.api_utils import pagination_metadata, filter_composes
from odcs.server.auth import requires_role, login_required
from odcs.server.auth import require_oidc_scope


api_v1 = {
    'composes': {
        'url': '/api/1/composes/',
        'options': {
            'defaults': {'id': None},
            'methods': ['GET'],
        }
    },
    'compose': {
        'url': '/api/1/composes/<int:id>',
        'options': {
            'methods': ['GET'],
        }
    },
    'composes_post': {
        'url': '/api/1/composes/',
        'options': {
            'methods': ['POST'],
        }
    },
    'composes_delete': {
        'url': '/api/1/composes/<int:id>',
        'options': {
            'methods': ['DELETE'],
        }
    },
}


class ODCSAPI(MethodView):
    def get(self, id):
        if id is None:
            p_query = filter_composes(request)

            json_data = {
                'meta': pagination_metadata(p_query, request.args),
                'items': [item.json() for item in p_query.items]
            }

            return jsonify(json_data), 200

        else:
            compose = Compose.query.filter_by(id=id).first()
            if compose:
                return jsonify(compose.json()), 200
            else:
                raise NotFound('No such compose found.')

    @login_required
    @requires_role('allowed_clients')
    def post(self):
        if conf.auth_backend == "noauth":
            owner = "unknown"
            log.warn("Cannot determine the owner of compose, because "
                     "'noauth' auth_backend is used.")
        else:
            owner = g.user.username

        data = request.get_json(force=True)
        if not data:
            raise ValueError('No JSON POST data submitted')

        if conf.auth_backend != "noauth":
            if 'id' in data:
                require_oidc_scope('renew-compose')
            else:
                require_oidc_scope('new-compose')

        seconds_to_live = conf.seconds_to_live
        if "seconds-to-live" in data:
            try:
                seconds_to_live_in_request = int(data['seconds-to-live'])
            except ValueError as e:
                err = 'Invalid seconds-to-live specified in request: %s' % data
                log.error(err)
                raise ValueError(err)

            seconds_to_live = min(seconds_to_live_in_request, conf.max_seconds_to_live)

        # If "id" is in data, it means client wants to regenerate an expired
        # compose.
        if "id" in data:
            old_compose = Compose.query.filter(
                Compose.id == data["id"],
                Compose.state.in_(
                    [COMPOSE_STATES["removed"],
                     COMPOSE_STATES["done"],
                     COMPOSE_STATES["failed"]])).first()

            if not old_compose:
                err = "No compose with id %s found" % data["id"]
                log.error(err)
                raise NotFound(err)

            state = old_compose.state
            if state in (COMPOSE_STATES['removed'], COMPOSE_STATES['failed']):
                log.info("%r: Going to regenerate the compose", old_compose)
                compose = Compose.create_copy(db.session, old_compose, owner,
                                              seconds_to_live)
                db.session.add(compose)
                db.session.commit()
                return jsonify(compose.json()), 200

            # Otherwise, just extend expiration to make it usable for longer time.
            extend_from = datetime.datetime.utcnow()
            old_compose.extend_expiration(extend_from, seconds_to_live)
            log.info('Extended time_to_expire for compose %r to %s',
                     old_compose, old_compose.time_to_expire)
            # As well as extending those composes that reuse this this compose,
            # and the one this compose reuses.
            reused_compose = old_compose.get_reused_compose()
            if reused_compose:
                reused_compose.extend_expiration(extend_from, seconds_to_live)
            for c in old_compose.get_reusing_composes():
                c.extend_expiration(extend_from, seconds_to_live)
            db.session.commit()
            return jsonify(old_compose.json()), 200

        source_data = data.get('source', None)
        if not isinstance(source_data, dict):
            err = "Invalid source configuration provided: %s" % str(data)
            log.error(err)
            raise ValueError(err)

        needed_keys = ["type", "source"]
        for key in needed_keys:
            if key not in source_data:
                err = "Missing %s in source configuration, received: %s" % (key, str(source_data))
                log.error(err)
                raise ValueError(err)

        source_type = source_data["type"]
        if source_type not in PUNGI_SOURCE_TYPE_NAMES:
            err = 'Unknown source type "%s"' % source_type
            log.error(err)
            raise ValueError(err)

        if source_type not in conf.allowed_source_types:
            err = 'Source type "%s" is not allowed by ODCS configuration' % (
                source_type)
            log.error(err)
            raise ValueError(err)

        source_type = PUNGI_SOURCE_TYPE_NAMES[source_type]

        source = source_data["source"].split(" ")
        if not source:
            err = "No source provided for %s" % source_type
            log.error(err)
            raise ValueError(err)
        source = ' '.join(filter(None, source))

        packages = None
        if "packages" in source_data:
            packages = ' '.join(source_data["packages"])

        sigkeys = ""
        if "sigkeys" in source_data:
            sigkeys = ' '.join(source_data["sigkeys"])
        else:
            sigkeys = ' '.join(conf.sigkeys)

        flags = 0
        if "flags" in data:
            for name in data["flags"]:
                if name not in COMPOSE_FLAGS:
                    raise ValueError("Unknown flag %s", name)
                flags |= COMPOSE_FLAGS[name]

        compose = Compose.create(
            db.session, owner, source_type, source,
            COMPOSE_RESULTS["repository"], seconds_to_live,
            packages, flags, sigkeys)
        db.session.add(compose)
        db.session.commit()

        return jsonify(compose.json()), 200

    @login_required
    @requires_role('admins')
    def delete(self, id):
        require_oidc_scope('delete-compose')

        compose = Compose.query.filter_by(id=id).first()
        if compose:
            # can remove compose that is in state of 'done' or 'failed'
            deletable_states = {n: COMPOSE_STATES[n] for n in ['done', 'failed']}
            if compose.state not in deletable_states.values():
                raise BadRequest('Compose (id=%s) can not be removed, its state need to be in %s.' %
                                 (id, deletable_states.keys()))

            # change compose.time_to_expire to now, so backend will
            # delete this compose as it's an expired compose now
            compose.time_to_expire = datetime.datetime.utcnow()
            db.session.add(compose)
            db.session.commit()
            message = ("The delete request for compose (id=%s) has been accepted and will be"
                       " processed by backend later." % compose.id)
            response = jsonify({'status': 202,
                                'message': message})
            response.status_code = 202
            return response
        else:
            raise NotFound('No such compose found.')


def register_api_v1():
    """ Registers version 1 of ODCS API. """
    module_view = ODCSAPI.as_view('composes')
    for key, val in api_v1.items():
        app.add_url_rule(val['url'],
                         endpoint=key,
                         view_func=module_view,
                         **val['options'])


register_api_v1()
