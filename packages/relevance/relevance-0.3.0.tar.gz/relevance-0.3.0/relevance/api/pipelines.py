"""
Relevance pipeline REST API.

This module provides the REST API for pipelines.
"""

import os
import pydoc
import anyconfig

from flask import request
from flask import jsonify
from flask import Response

from relevance.api import Flask
from relevance.api import start_app
from relevance.pipeline import Pipeline


# Register the application
app = Flask('relevance.api.pipelines')

# The configuration objects
app.data = type('app_data', (object,), dict(
    config={},
    pipelines={},
))()


def load_config(env_name: str=None):
    """
    Load or reload the configuration.

    :param env_name: the name of the environment to load. If omitted, it is taken
    from the PYTHON_ENV environment variable. If it doesn't exist, 'development' is
    assumed.
    """
    if env_name is None:
        env_name = os.environ.get('PYTHON_ENV', 'development')

    # Load the configuration file
    this_config = anyconfig.load(
        ['./etc/pipelines.json', './etc/pipelines.{0}.json'.format(env_name)],
        ignore_missing=True,
    )

    # Load the pipeline instances
    this_items = {}
    for name, target in this_config.get('pipelines', {}).items():
        loader = pydoc.locate(target)

        pipe = loader()
        if not isinstance(pipe, Pipeline):
            raise ImportError('cannot load pipeline from {0}'.format(target))

        this_items[name] = pipe

    app.data.config.clear()
    app.data.config.update(this_config)
    app.data.pipelines.clear()
    app.data.pipelines.update(this_items)


def load_plugins():
    """
    Load or reload the plugins.
    """
    for plugin in app.data.config.get('plugins', []):
        func = pydoc.locate(plugin)
        if func is None:
            raise ImportError('cannot load plugin {0}'.format(plugin))

        func(app)


@app.route('/', methods=['GET'])
def get_config() -> Response:
    """
    Get the configuration.
    """
    data = list(app.data.config.keys())
    response = jsonify(data)
    response.status_code = 201
    return response


@app.route('/<pipeline_name>', methods=['GET'])
def get_pipeline_info(pipeline_name: str) -> Response:
    """
    Get information about a pipeline.

    :param pipeline_name: the name of the pipeline to check.

    Returns a status object.
    """
    try:
        pipeline = app.data.pipelines[pipeline_name]
    except KeyError:
        response = jsonify({
            'error': {
                'desc': 'pipeline not found',
                'key': pipeline_name,
                'code': 'PipelineNotFound',
            }
        })
        response.status_code = 404
        return response

    try:
        input_status = pipeline.extractor.input_status or {}
    except AttributeError:
        input_status = {'size': pipeline.extractor.qsize()}

    try:
        output_status = pipeline.publisher.output_status or {}
    except AttributeError:
        output_status = {}

    data = {
        'type': '{0}.{1}'.format(pipeline.__class__.__module__, pipeline.__class__.__name__),
        'target': app.data.config[pipeline_name],
        'input': input_status,
        'output': output_status,
    }

    response = jsonify(data)
    response.status_code = 200
    return response


# @app.errorhandler(QueryParserError)
# def parser_error(ex: QueryParserError) -> Response:
#     """
#     Handle parse errors.
#     """
#     response = jsonify({
#         'error': {
#             'desc': str(ex),
#             'code': 'QueryParserError',
#         }
#     })
#     response.status_code = 400
#     return response
#
#
@app.after_request
def app_cors(response: Response) -> Response:
    """
    CORS request handler.

    Adds the CORS headers to all responses so that the API can be used directly from
    a web browser.
    """
    headers = {
        'Access-Control-Allow-Origin': request.headers.get('Origin', '*'),
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': 'POST, OPTIONS, GET, PUT, DELETE, HEAD, TRACE',
        'Access-Control-Allow-Headers': request.headers.get(
            'Access-Control-Request-Headers', 'Authorization'
        ),
    }

    for k, v in headers.items():
        response.headers[k] = v

    if app.debug:
        response.headers['Access-Control-Max-Age'] = '1'

    return response


if __name__ == '__main__':
    load_config()
    load_plugins()
    start_app(app)
