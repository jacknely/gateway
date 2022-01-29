"""Tests for the /health endpoints."""
import pytest


def test_ping(app):
    """Test the ping endpoint returns the expected 200, 'Pong' response."""
    response = app.get('/health/ping')

    assert response.status_code == 200
    assert 'Pong' in str(response.data)


def test_output_logs(app, caplog):
    """Test the output-logs endpoint outputs the expected logs."""
    with caplog.at_level(app.application.config['LOG_LEVEL']):
        response = app.get('/health/output-logs')
        logs = caplog.text

        assert response.status_code == 200
        assert 'Logs outputted' in str(response.data)

        assert 'A debug message' in logs
        assert 'And info message with some extra' in logs
        assert 'A warning message' in logs
        assert 'An error message, with extra and stack trace' in logs


def test_raise_exception(app):
    """Test the raise-exception endpoint raises the correct exception."""
    with pytest.raises(Exception) as e:
        app.get('/health/raise-exception')

    assert str(e.value) == 'TEST: This is a test exception!'
