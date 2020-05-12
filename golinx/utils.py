"""These are utils to help out with various things in the application.
"""
from typing import Union

import flask
from flask import views


RESERVED_ROUTES = [
        'all',
        'new',
        'search',
        'query',
]


def register_resource(
        resource: Union[flask.Flask, flask.Blueprint],
        view: Union[views.MethodView, views.View],
        endpoint: str,
        url: str = '',
        suffix: str = '',
        pk: str = 'id',
        pk_type: str = 'int'
    ) -> None:
    """Registers rest-like routes on a view class.

    Set the URL without a trailing slash, because one will be added where needed.
    
    Set the suffix argument to distinguish something like JSON APIs from their
    corresponding HTML versions.
    """
    view_func = view.as_view(endpoint)

    # Basically a list view.
    resource.add_url_rule('{}/{}'.format(url, suffix), defaults={pk: None},
            view_func=view_func, methods=['GET'])

    # Create
    resource.add_url_rule(
            '{}/{}'.format(url, suffix), view_func=view_func, methods=['POST'])

    # Read, Update, Destroy
    resource.add_url_rule(
            '{}/<{}:{}>{}'.format(url, pk_type, pk, suffix), view_func=view_func,
            methods=['GET', 'PUT', 'DELETE'])
