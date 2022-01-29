"""Tests to check the app can load and function correctly."""

from flask import request


def test_app_can_load_and_ping(app):
    """Test the application can load and accept requests."""
    response = app.get('/health/ping')

    assert response.status_code == 200
    assert 'Pong' in str(response.data)


def test_proxy_fix_gives_us_https_urls(app):
    """Test calling view endpoints are https to flask internally.

    We use the ProxyFix class in app_setup to handle the X-Forwarded-Proto
    header so internally it knows it's running in a https environment. This
    tests checks that internally Flask knows this is the case.
    """
    app.get('/health/ping', headers={'X-Forwarded-Proto': 'https'})

    assert request.scheme == 'https'
    assert request.url == 'https://localhost/health/ping'
    assert request.base_url == 'https://localhost/health/ping'


def test_app_loads_base_config_correctly(app):
    """Test the base config values are loaded regardless of environment."""
    assert app.application.config['LOG_LEVEL'] == 'DEBUG'


def test_app_loads_env_config_correctly(app):
    """Test the environment specific config is loaded in."""
    assert app.application.config['TEST_CONFIG'] == 'foobar'
