import functools

import flask
from flask import views

from golinx.db import get_db
from golinx.db import utils

link_blueprint = Blueprint('link', __name__, url_prefix='/links')

class LinkView(views.MethodView):
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

link_view = LinkView.as_view('link')
utils.register_resource(
        link_blueprint, LinkView, 'link', '/', pk='link_id', pk_type='string')
