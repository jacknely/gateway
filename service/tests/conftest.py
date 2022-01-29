"""Collection of fixtures accessible globally to all test methods."""
import pytest

from service import app as application


@pytest.fixture()
def app():
    """Provide a testing Flask application for view testing with seeded data.

    This also provides an authenticated user so it can be used for testing
    endpoints that have the @login_required decorator applied to them.

    To get the original application, for example it's config variables you can
    call `app.application` on the fixture. i.e `app.application.config`.

    Example Usage:
        def test_foo_view_endpoint_returns_foo_bar_list(app):
            response = app.get('/foo')

            assert response.status_code == 200
            assert json.loads(response.data) == ['foo', 'bar']
    """
    with application.test_client() as context:
        yield context
