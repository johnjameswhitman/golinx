import functools
import json

import flask
from flask import views

from golinx import utils


ENDPOINT_NAME = 'link'
URL_PREFIX = '/links'


class LinkHtmlView(views.MethodView):
    def get(self, link_id: str) -> str:
        """Gets all or one link record."""
        if link_id is None:
            link_ids = ['a', 'b', 'c']
            return ', '.join(link_ids)
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


class LinkJsonView(views.MethodView):
    def get(self, link_id: str) -> str:
        """Gets all or one link record."""
        if link_id is None:
            link_ids = list({'link_id': v} for v in ['a', 'b', 'c'])
            return json.dumps(link_ids)
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
            ENDPOINT_NAME, __name__, url_prefix=URL_PREFIX)

    utils.register_resource(blueprint, LinkHtmlView, ENDPOINT_NAME,
            pk='link_id', pk_type='string')

    utils.register_resource(blueprint, LinkJsonView, ENDPOINT_NAME + '_json',
            suffix='.json', pk='link_id', pk_type='string')

    return blueprint
