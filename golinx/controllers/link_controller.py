"""Controllers that generate views for the link resource."""
import html
import json
import re

import flask
from flask import views

from golinx import utils
from golinx.models import db
from golinx.models import base_model
from golinx.models import link_model


BLUEPRINT_NAME = 'link'
URL_PREFIX = '/links'


class LinkHtmlController(views.MethodView):
    ENDPOINT_NAME = 'link'

    # TODO(john): Create `index` method separately.
    def get(self, link_id: str) -> str:
        """Gets all or one link record."""
        if link_id is None:
            links = link_model.LinkModel.all(db.get_db())
            # return {'data': [item.as_dict(serialize_date=True) for item in links]}
            return flask.render_template('link/index.html', links=links)
        elif link_id == 'new':
            return flask.render_template('link/new.html')
        else:
            link = link_model.LinkModel.get(db.get_db(), link_id)
            return flask.render_template('link/get.html', link=link)

    def put(self, link_id: str) -> str:
        """Updates existing link."""
        return link_id

    def post(self) -> str:
        """Creates new link."""
        # TODO(john): Factor out validation.
        if 'shortlink' in flask.request.form and flask.request.form.getlist('shortlink')[0] == 'shortlink':
            link_type = link_model.LinkType.SHORT.name
        else:
            link_type = link_model.LinkType.CUSTOM.name
            if not flask.request.form['shortcut']:
                flask.abort(400)

            original_path = flask.request.form['shortcut']
            canonical_path = re.sub(
                link_model.LinkModel.canonical_path_ignored_chars, '', original_path)
        
        link = link_model.LinkModel(
            db=db.get_db(),
            owner_id=1,  # TODO(john), fix this once users implemented.
            created_by=1,  # TODO(john), fix this once users implemented.
            updated_by=1,  # TODO(john), fix this once users implemented.
            link_type=link_type,
            original_path=original_path,
            canonical_path=canonical_path,
            destination=flask.request.form['destination'],
            title=html.escape(flask.request.form['title']),
            description=html.escape(flask.request.form['description'])
        )

        try:
            link_id = link.save()
            print('Link id is ', link_id)
            # TODO(john): Dive into url_for impl to understand conflict w/ querystring.
            # Essentially, it ends up here:
            # - https://github.com/pallets/flask/tree/master/src/flask#L211 (url_for)
            # - https://github.com/pallets/werkzeug/blob/master/src/werkzeug/routing.py#L2060 (url_map.build)
            #
            # While I figure this out, create a "ResourceController" base class that handles this bs.
            print('URL is ', flask.url_for('.link', link_id=str(link_id)))
            print('URL Map is ', str(flask._request_ctx_stack.top.url_adapter.map))
            return flask.redirect(flask.url_for('.link', link_id=str(link_id)), code=303)
        except base_model.ModelError as e:
            flask.flash(str(e))
            # TODO(john): Repopulate form with old data.
            return flask.redirect(flask.url_for('.link_item', link_id='new'), code=303)

    def delete(self, link_id: str) -> str:
        """Deletes the link."""
        return 'fake delete of {}'.format(link_id)


def create_blueprint() -> flask.Blueprint:
    """Provides the link-resource blueprint, ready for use."""
    blueprint = flask.Blueprint(
        BLUEPRINT_NAME,
        __name__,
        url_prefix=URL_PREFIX)

    utils.register_resource(blueprint, LinkHtmlController, LinkHtmlController.ENDPOINT_NAME,
                            pk='link_id', pk_type='string')

    return blueprint
