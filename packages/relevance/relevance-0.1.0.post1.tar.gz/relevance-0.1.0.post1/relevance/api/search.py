"""
Relevance search REST API.

This module provides the REST API for search.
"""

import os
import pydoc
import anyconfig

from flask import request
from flask import jsonify
from flask import Response

from relevance.api import Flask
from relevance.api import start_app
from relevance.query import QueryParser
from relevance.query import QueryParserError
from relevance.facet import Facet
from relevance.engine import SearchEngine


# Register the application
app = Flask('relevance.api.search')

# The configuration objects
config = {}
engines = {}


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
    this_config = anyconfig.load(['./etc/default.json', './etc/{0}.json'.format(env_name)],
                                 ignore_missing=True)
    config.clear()
    config.update(this_config)

    # Load the engine instances
    this_engines = {}
    for engine_name, conf in config.items():
        try:
            cls_name = conf['engine']
            target = conf['target']
        except KeyError as ex:
            raise KeyError('missing configuration key {0}'.format(str(ex)))

        cls = pydoc.locate(cls_name)
        if cls is None or not issubclass(cls, SearchEngine):
            raise ImportError('cannot find engine {0}'.format(cls_name))

        facets = {}
        for facet_name, facet_conf in conf.get('facets', {}).items():
            facet_cls = pydoc.locate(facet_conf.get('type'))
            if facet_cls is None or not issubclass(facet_cls, Facet):
                raise ImportError('cannot find facet {0}'.format(facet_conf['type']))

            facet_obj = facet_cls(
                field=facet_conf.get('field'),
                path=facet_conf.get('path'),
                **facet_conf.get('options', {}),
            )

            facets[facet_name] = facet_obj

        options = conf.get('options', {})
        this_engines[engine_name] = cls(target, facets=facets, **options)

    engines.clear()
    engines.update(this_engines)


# Load the configuration initially
load_config()


@app.route('/<engine_name>', methods=['GET'])
def do_search(engine_name: str) -> Response:
    """
    Perform a search request.

    Request arguments:
        q -- the query to run.

    .. seealso: :py:class:`QueryParser`

    :param engine_name: the name of the engine to use.
    """
    try:
        engine = engines[engine_name]
    except KeyError:
        response = jsonify({
            'error': {
                'desc': 'engine not found',
                'key': engine_name,
                'code': 'EngineNotFound',
            }
        })
        response.status_code = 404
        return response

    query = request.args.get('q', '')
    search = QueryParser().loads(query)

    results = engine.search(search)
    data = {
        'search': search.to_dict(),
        'results': results,
        'time': results.time,
        'count': results.count,
    }

    if results.facets is not None:
        data.update({
            'facets': results.facets,
        })

    response = jsonify(data)
    response.status_code = 200
    return response


@app.errorhandler(QueryParserError)
def parser_error(ex: QueryParserError) -> Response:
    """
    Handle parse errors.
    """
    response = jsonify({
        'error': {
            'desc': str(ex),
            'code': 'QueryParserError',
        }
    })
    response.status_code = 400
    return response


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
    start_app(app)
