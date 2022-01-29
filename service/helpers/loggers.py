"""Custom loggers used by the service."""
import os
from collections import OrderedDict
from typing import Optional

from gunicorn import glogging
from gunicorn.config import Config
from pythonjsonlogger import jsonlogger

from service.constants import SERVICE_NAME


class DatadogLogFormatter(jsonlogger.JsonFormatter):
    """Generic logger for formatting our datadog logs.

    This creates json formatted logs for datadog with extra attributes
    injected such as the service name, application stage and source.

    This is not generally meant for instantiation but for extending and then
    overriding the fmt and source class level attributes.
    """

    source: Optional[str] = None
    service: str = SERVICE_NAME
    fmt: str = (
        '%(asctime)s %(levelname)s %(message)s'
        '[dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s]'
    )

    def __init__(self, *args, **kwargs):
        """Construct a DatadogLogFormatter object."""
        super(DatadogLogFormatter, self).__init__(
            fmt=self.fmt, *args, **kwargs
        )

    def process_log_record(self, log_record: OrderedDict) -> OrderedDict:
        """Pre-process the log record adding extra custom attributes.

        These extra attributes will get added to the final logs and then
        formatted to json meaning they can be picked up by datadog.

        Args:
            log_record: The original log record.

        Returns:
            The log record with our additional attributes.
        """
        log_record['log_source'] = self.source
        log_record['service'] = self.service
        log_record['dd.span_id'] = str(log_record['dd.span_id'])
        log_record['dd.trace_id'] = str(log_record['dd.trace_id'])
        log_record['application_stage'] = os.environ.get('APPLICATION_STAGE')
        log_record['status'] = log_record['levelname']

        return (
            super(DatadogLogFormatter, self)
            .process_log_record(log_record=log_record)
        )


class DatadogGunicornErrorLogFormatter(DatadogLogFormatter):
    """Formatter for formatting gunicorn error logs for datadog."""

    source: str = 'gunicorn'


class DatadogFlaskLogFormatter(DatadogLogFormatter):
    """Formatter for formatting flask logs for datadog."""

    source: str = 'flask'


class DatadogGunicornLogger(glogging.Logger):
    """Custom logger for Gunicorn log messages."""

    def setup(self, cfg: Config) -> None:
        """Configure Gunicorn application logging configuration.

        We override the formatter used for both the gunicorn error and
        application logs, adding further attributes for datadog.

        Args:
            cfg: A gunicorn configuration object.
        """
        super(DatadogGunicornLogger, self).setup(cfg=cfg)

        self._set_handler(
            log=self.error_log,
            output=cfg.errorlog,
            fmt=DatadogGunicornErrorLogFormatter()
        )
