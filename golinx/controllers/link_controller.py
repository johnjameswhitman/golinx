"""Controllers that generate views for the link resource."""
import json

import flask
from flask import views

from golinx import utils
from golinx.models import db
from golinx.models import link_model


ENDPOINT_NAME = 'link'
URL_PREFIX = '/links'


class LinkHtmlController(views.MethodView):
    def get(self, link_id: str) -> str:
        """Gets all or one link record."""
        if link_id is None:
            links = link_model.LinkModel.all(db.get_db())
            # return {'data': [item.as_dict(serialize_date=True) for item in links]}
            return flask.render_template('link/index.html', links=links)
        else:
            return link_id

    def put(self, link_id: str) -> str:
        """Updates existing link."""
        return link_id

    def post(self) -> str:
        """Creates new link."""
        return 'nothing done yet.'

    def delete(self, link_id: str) -> str:
        """Deletes the link."""
        return 'fake delete of {}'.format(link_id)


class LinkJsonController(views.MethodView):
    def get(self, link_id: str) -> str:
        """Gets all or one link record."""
        if link_id is None:
            return {'data': [item.as_dict(serialize_date=True) for item in link_model.LinkModel.all(db.get_db())]}
        else:
            return json.dumps({'link_id': link_id})

    def put(self, link_id: str) -> str:
        """Updates existing link."""
        return link_id

    def post(self) -> str:
        """Creates new link."""
        return 'nothing done yet.'

    def delete(self, link_id: str) -> str:
        """Deletes the link."""
        return 'fake delete of {}'.format(link_id)


def create_blueprint() -> flask.Blueprint:
    """Provides the link-resource blueprint, ready for use."""
    blueprint = flask.Blueprint(
        ENDPOINT_NAME,
        __name__,
        url_prefix=URL_PREFIX)

    utils.register_resource(blueprint, LinkHtmlController, ENDPOINT_NAME,
                            pk='link_id', pk_type='string')

    utils.register_resource(blueprint, LinkJsonController, ENDPOINT_NAME + '_json',
                            suffix='.json', pk='link_id', pk_type='string')

    return blueprint
