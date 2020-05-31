"""Base controller that generates views for a RESTful resource.

See ResourceController.as_blueprint() for a list of the routes this provides.

A few improvements that could be made include:
- For improved readability and testability, it would be nice if the controller CRUD methods
  used meaningful representations of their requests and response objects in the signature,
  e.g. `FooController.update(FooRequest) -> FooResponse`, where FooRequest and FooResponse also
  sub-type a ResourceRequest and ResourceResponse akin to ResourceController.
- Ability to nest one resource inside another. Ideally you'd be able to dynamically compose
  resources, which means you:
  - Write each resources' controller independently.
  - Register a child-resource's controller under a parent.
  - Decouple the controller implementation from the underlying models, which shouldn't need to
    know about controller details. In other words, there should be a clear and clean dependency
    hierarchy from app -> controller -> model (no downward dependencies, clear boundaries).
- Remove the 1:1 relationship between blueprint and resource (easy). The blueprint should still
  be what you register with the application, but a blueprint should be a composition of resources.
"""
import flask
from flask import views


class ItemIdTypes(object):
    UNKOWN: str = 'unknown'
    STRING: str = 'string'
    INT: str = 'int'
    FLOAT: str = 'float'
    PATH: str = 'path'
    UUID: str = 'uuid'


class ResourceController(views.MethodView):
    """A base resource controller for rest-like interactions.

    To get this up and running, inherit and override the following methods:
    - index
    - search
    - create
    - read
    - update
    - destroy
    The standard HTTP verbs just pass through to their CRUD equivalents.

    To access request data outside of the item_id, methods still need to tap into flask.request.
    See the module docstring for thoughts on this.
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
        """Generates blueprint for the controller.

        The blueprint will have routes that support the CRUD operations for the resource:
        - METHOD /path/ -> endpoint name, method
        - List
            - GET /{resource}/ -> {resource}.index, cls.index
            - GET /{resource}/search -> {resource}.search, cls.search
        - Create
            - POST /{resource}/ -> {resource}.item, cls.post (proxies .create)
        - Read
            - GET /{resource}/{item_id} -> {resource}.item, cls.get (proxies .read)
        - Update
            - PUT /{resource}/{item_id} -> {resource}.item, cls.put (proxies .update)
            - POST /{resource}/{item_id}/update -> {resource}.update, cls.update
        - Destroy
            - DELETE /{resource}/{item_id} -> {resource}.item, cls.delete (proxies .destroy)
            - POST /{resource}/{item_id}/destroy -> {resource}.destroy, cls.destroy

        The proxy routes on update and destroy allow you to use basic HTML forms, which only
        support the POST method. Prefer to use the PUT and DELETE {resource}.item endpoints with
        API clients that support them.
        """
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
            '/<{}:item_id>{}'.format(cls.ITEM_ID_TYPE, cls.SUFFIX),
            view_func=item_handler,
            methods=['GET', 'PUT', 'DELETE'])

        # For HTML forms, provide explicit POST endpoints to UPDATE and DELETE since these verbs not
        # supported by browsers.
        blueprint.add_url_rule(
            '/<{}:item_id>/update{}'.format(cls.ITEM_ID_TYPE, cls.SUFFIX),
            endpoint='update',
            view_func=cls.update,
            methods=['POST'])

        blueprint.add_url_rule(
            '/<{}:item_id>/destroy{}'.format(cls.ITEM_ID_TYPE, cls.SUFFIX),
            endpoint='destroy',
            view_func=cls.destroy,
            methods=['POST'])

        return blueprint
