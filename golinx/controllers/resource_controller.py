"""Controllers that generate views for the link resource."""
import flask
from flask import views


class ItemIdTypes(object):
    UNKOWN: str = 'unknown'
    STRING: str = 'string'
    INT: str = 'int'
    FLOAT: str = 'float'
    PATH: str = 'path'
    UUID: str = 'uuid'

    def __repr__(self) -> str:
        """Merely provides the value as the string."""
        return self.value


class ResourceController(views.MethodView):
    """A base resource controller for rest-like interactions.

    To get this up and running, override the following methods:
    - index
    - search
    - create
    - read
    - update
    - destroy

    The standard http verbs just pass through to their CRUD equivalents.
    """
    RESOURCE_NAME = 'NEED_TO_OVERRIDE_RESOURCE_NAME'
    URL_PREFIX = '/NEED_TO_OVERRIDE_URL_PREFIX'
    ITEM_ID_TYPE = ItemIdTypes.INT
    SUFFIX = None

    def post(self) -> str:
        """Creates new item."""
        return self.create()

    def get(self, item_id: str) -> str:
        """Gets one item."""
        return self.read(item_id)

    def put(self, item_id: str) -> str:
        """Updates existing item."""
        return self.update(item_id)

    def delete(self, item_id: str) -> str:
        """Deletes the item."""
        return self.destroy(item_id)

    @staticmethod
    def index() -> str:
        """Index page for all items."""
        raise NotImplementedError('Implement in subclass.')

    @staticmethod
    def search() -> str:
        """Searches for items using query-string."""
        raise NotImplementedError('Implement in subclass.')

    @staticmethod
    def create() -> str:
        """Proxy put method."""
        raise NotImplementedError('Implement in subclass.')

    @staticmethod
    def read(item_id: str) -> str:
        """Proxy put method."""
        raise NotImplementedError('Implement in subclass.')

    @staticmethod
    def update(item_id: str) -> str:
        """Proxy put method."""
        raise NotImplementedError('Implement in subclass.')

    @staticmethod
    def destroy(item_id: str) -> str:
        """Proxy delete method."""
        raise NotImplementedError('Implement in subclass.')

    @classmethod
    def as_blueprint(cls) -> flask.Blueprint:
        """Generates blueprint for the controller."""
        blueprint = flask.Blueprint(
            cls.RESOURCE_NAME,
            __name__,
            url_prefix=cls.URL_PREFIX)

        # Index view.
        index_path = '/all{}'.format(cls.SUFFIX) if cls.SUFFIX else '/'
        blueprint.add_url_rule(index_path, endpoint='index', view_func=cls.index, methods=['GET'])

        # Search view.
        blueprint.add_url_rule(
            '/search{}'.format(cls.SUFFIX),
            endpoint='search',
            view_func=cls.search,
            methods=['GET'])

        # Create item.
        item_handler = cls.as_view('item')  # Establishes item endpoint name.
        blueprint.add_url_rule('/', view_func=item_handler, methods=['POST'])

        # Read, Update, Destroy existing item.
        blueprint.add_url_rule(
            '/<{}:item_id>{}'.format(cls.ITEM_ID_TYPE.value, cls.SUFFIX),
            view_func=item_handler,
            methods=['GET', 'PUT', 'DELETE'])
        
        # For HTML forms, provide explicit POST endpoints to UPDATE and DELETE since these verbs not
        # supported by browsers.
        blueprint.add_url_rule(
            '/<{}:item_id>/update{}'.format(cls.ITEM_ID_TYPE.value, cls.SUFFIX),
            endpoint='update',
            view_func=cls.update,
            methods=['GET', 'POST'])

        blueprint.add_url_rule(
            '/<{}:item_id>/delete{}'.format(cls.ITEM_ID_TYPE.value, cls.SUFFIX),
            endpoint='delete',
            view_func=cls.destroy,
            methods=['GET', 'POST'])

        return blueprint