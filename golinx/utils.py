"""These are utils to help out with various things in the application.
"""
import flask

def register_resource(
        resource: Union[flask.Flask, flask.Blueprint],
        view: Union[flask.views.MethodView, flask.views.View],
        endpoint: str,
        url: str,
        pk: str = 'id',
        pk_type: str ='int'
    ) -> None:
    view_func = view.as_view(endpoint) 
    resource.add_url_rule(
            url, defaults={pk: None}, view_func=view_func, methods=['GET'])
    resource.add_url_rule(
            url, view_func=view_func, methods=['POST'])
    resource.add_url_rule(
            '{}<{}:{}>'.format(url, pk_type, pk), view_func=view_func,
            methods=['GET', 'PUT', 'DELETE'])
