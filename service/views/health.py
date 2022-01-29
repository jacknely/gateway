"""Collection of health endpoints for the service."""
import logging

from flask import Blueprint

from service.constants import SERVICE_NAME

bp = Blueprint('health', __name__, url_prefix='/health')


@bp.route('')
@bp.route('/ping')
def ping():
    """Return a 200 pong response to check the application is responding."""
    return 'Pong', 200


@bp.route('/raise-exception')
def raise_exception():
    """Raise an un-caught exception."""
    raise Exception('TEST: This is a test exception!')


@bp.route('/output-logs')
def output_logs():
    """Output various levels of logs with messages and extra info."""
    logger = logging.getLogger(SERVICE_NAME)

    logger.debug('A debug message')
    logger.info(
        'And info message with some extra',
        extra={
            'key': 'value',
            'second-key': 'second value',
        }
    )
    logger.warning('A warning message')
    logger.error(
        'An error message, with extra and stack trace',
        extra={
            'key': 'value',
            'second-key': 'second value',
        },
        exc_info=True
    )

    return 'Logs outputted', 200
