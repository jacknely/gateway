"""Setup the Flask application and all the required infrastructure."""
import logging
import os
import sys
import json

import graphene
from flask import Flask
from flask_graphql import GraphQLView
from werkzeug.middleware.proxy_fix import ProxyFix

import service.views
from service.constants import SERVICE_NAME
from service.infrastructure.graphql import Query


def app_setup(app: Flask) -> None:
    """Setup all the relevant parts of a Flask application.

    Args:
        app: The base Flask application to setup.
    """
    env = os.environ['APPLICATION_STAGE']

    _configure_app(app=app, env=env)
    _configure_logging(app=app)
    _register_views(app=app)

    # As the application runs behind a proxy server, ensure flask knows how
    # to handle this internally via ProxyFix. See below for more details:
    # http://flask.pocoo.org/docs/1.0/deploying/wsgi-standalone/#proxy-setups
    setattr(app, 'wsgi_app', ProxyFix(app.wsgi_app, x_proto=1))


def _configure_app(app: Flask, env: str) -> None:
    """Configure environment specific config for a Flask application.

    Args:
        app: The base Flask application to add configuration to.
        env: The current environment.
    """
    app_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(app_path, 'config')

    app.config.from_file(
        filename=os.path.join(f'{config_path}/base.json'), load=json.load
    )
    app.config.from_file(
        filename=os.path.join(f'{config_path}/{env}.json'),
        load=json.load,
        silent=True
    )
    app.config.from_file(
        filename=os.path.join(f'{config_path}/local.json'),
        load=json.load,
        silent=True
    )


def _configure_logging(app: Flask) -> None:
    """Configure logging for a Flask application.

    Args:
        app: The Flask application to configure logging for.
    """
    handler = logging.StreamHandler(sys.stdout)
    logger = logging.getLogger(SERVICE_NAME)
    logger.setLevel(level=app.config['LOG_LEVEL'])
    logger.addHandler(handler)


def _register_views(app: Flask) -> None:
    """Register views for a Flask application.

    Args:
        app: The Flask application to set the views up for.
    """
    app.add_url_rule(
        rule='/graphql',
        view_func=GraphQLView.as_view(
            name='graphql',
            schema=graphene.Schema(query=Query),
            graphiql=True
        )
    )

    for bp in service.views.VIEW_BLUEPRINTS:
        app.register_blueprint(bp)


app = Flask(__name__)
app_setup(app)
