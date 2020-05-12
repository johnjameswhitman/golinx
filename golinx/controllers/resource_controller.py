"""Controllers that generate views for the link resource."""
import enum

import flask
from flask import views


class ItemIdTypes(enum.Enum):
    UNKOWN = 'unknown'
    STRING = 'string'
    INT = 'int'
    FLOAT = 'float'
    PATH = 'path'
    UUID = 'uuid'

    def __repr__(self) -> str:
        """Merely provides the value as the string."""
        return self.value


class ResourceController(views.MethodView):
    RESOURCE_NAME = 'NEED_TO_OVERRIDE_RESOURCE_NAME'
    URL_PREFIX = '/NEED_TO_OVERRIDE_URL_PREFIX'
    ITEM_ID_TYPE = ItemIdTypes.INT
    SUFFIX = None

    @staticmethod
    def index() -> str:
        """Index page for all items."""
        raise NotImplementedError('Implement in subclass.')

    @staticmethod
    def search() -> str:
        """Searches for items using query-string."""
        raise NotImplementedError('Implement in subclass.')

    def get(self, item_id: str) -> str:
        """Gets one item."""
        raise NotImplementedError('Implement in subclass.')

    def put(self, item_id: str) -> str:
        """Updates existing item."""
        raise NotImplementedError('Implement in subclass.')

    def post(self) -> str:
        """Creates new item."""
        raise NotImplementedError('Implement in subclass.')

    def delete(self, item_id: str) -> str:
        """Deletes the item."""
        raise NotImplementedError('Implement in subclass.')

    @classmethod
    def as_blueprint(cls) -> flask.Blueprint:
        """Generates blueprint for the controller."""
        blueprint = flask.Blueprint(
            cls.RESOURCE_NAME,
            __name__,
            url_prefix=cls.URL_PREFIX)

        index_path = '/all{}'.format(cls.SUFFIX) if cls.SUFFIX else '/'
        item_handler = cls.as_view('item')

        # Index view.
        blueprint.add_url_rule(index_path, endpoint='index', view_func=cls.index, methods=['GET'])

        # Search view.
        blueprint.add_url_rule(
            '/search{}'.format(cls.SUFFIX),
            endpoint='search',
            view_func=cls.search,
            methods=['GET'])

        # Create item.
        blueprint.add_url_rule('/', view_func=item_handler, methods=['POST'])

        # Read, Update, Destroy existing item.
        blueprint.add_url_rule(
            '/<{}:item_id>{}'.format(cls.ITEM_ID_TYPE.value, cls.SUFFIX),
            view_func=item_handler,
            methods=['GET', 'PUT', 'DELETE'])

        return blueprint