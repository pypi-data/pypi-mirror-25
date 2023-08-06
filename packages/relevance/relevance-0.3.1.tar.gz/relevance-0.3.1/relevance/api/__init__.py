"""
Relevance API package.

This package provides some common interfaces for the different REST APIs to use.
"""

import logging
from flask import Flask
from flask import request


def start_app(app: Flask):
    """
    Start an API application.

    :param app: the application object.
    """
    init_logger(app)
    app.run()


def init_logger(app: Flask):
    """
    Enable the API logger.

    :param app: the application object.
    """
    logger = logging.getLogger(app.name)

    @app.before_request
    def logger_before():
        logger.info('received {0} "{1}" with {2} bytes of {3}'.format(
            request.method, request.full_path, len(request.data),
            request.headers.get('Content-Type', 'unknown'),
        ))
        logger.debug('received {0} "{1}": {2}'.format(
            request.method, request.url, request.data,
        ))

    @app.after_request
    def logger_after(response):
        logger.info('response {0} "{1}" {2} with {3} bytes of {4}'.format(
            request.method, request.full_path, response.status_code, len(response.data),
            response.headers.get('Content-Type', 'unknown'),
        ))
        logger.debug('response {0} "{1}" {2}: {3}'.format(
            request.method, request.url, response.status_code, response.data,
        ))
        return response
