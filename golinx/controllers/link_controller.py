"""Controllers that generate views for the link resource."""
import html
import re

import flask

from golinx import utils
from golinx.controllers import resource_controller
from golinx.models import db
from golinx.models import base_model
from golinx.models import link_model


class LinkController(resource_controller.ResourceController):
    RESOURCE_NAME = 'link'
    URL_PREFIX = '/links'
    ITEM_ID_TYPE = resource_controller.ItemIdTypes.STRING
    SUFFIX = ''

    @staticmethod
    def index() -> str:
        """Overrides index method on parent."""
        links = [l for l in link_model.LinkModel.all(db.get_db())]
        print(links)
        return flask.render_template('link/index.html', links=links)

    @staticmethod
    def create() -> str:
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
            item_id = link.save()
            print(link)
            return flask.redirect(flask.url_for('.item', item_id=str(item_id), _method='GET'), code=303)
        except base_model.ModelError as e:
            flask.flash(str(e))
            # TODO(john): Repopulate form with old data.
            return flask.redirect(flask.url_for('.item', item_id='new'), code=303)

    @staticmethod
    def read(item_id: str) -> str:
        """Gets all or one link record."""
        if item_id == 'new':
            return flask.render_template('link/new.html')
        else:
            link = link_model.LinkModel.get(db.get_db(), item_id)
            return flask.render_template('link/get.html', link=link)

    @staticmethod
    def update(item_id: str) -> str:
        """Updates existing link."""
        return item_id

    @staticmethod
    def destroy(item_id: str) -> str:
        """Deletes the link."""
        link = link_model.LinkModel.get(db.get_db(), int(item_id))
        link.soft_delete()
        return flask.redirect(flask.url_for('.index', _method='GET'), code=303)