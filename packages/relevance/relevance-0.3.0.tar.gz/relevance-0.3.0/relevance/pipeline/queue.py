"""
Relevance pipeline REST module.

This module provides helper functions and the likes to make pipelines interact
with RESTful endpoints.
"""

import json
import pickle
from flask import request
from flask import jsonify
from flask import Response
from queue import Queue
from werkzeug import exceptions

from relevance.pipeline import Extractor
from relevance.api.pipelines import app


class QueueExtractor(Queue, Extractor):
    """
    Queue extractor.

    This class provides an extractor that wraps a queue that can be populated via
    an API.
    """
    def get_status(self):
        """
        Get additional state for the extractor.
        """
        return {
            'size': self.qsize(),
        }


@app.route('/<pipeline_name>', methods=['PUT'])
def put_document(pipeline_name: str) -> Response:
    """
    Put a document in the queue.

    Request payload:
        content -- the content to parse.
        type -- a MIME type of parse the content as. When None, the content is assumed
        to be a valid JSON object that can be fed directly into a document object.

    Returns a 202 response on success.
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

    if not isinstance(pipeline, QueueExtractor):
        raise exceptions.MethodNotAllowed()

    payload = request.get_json()
    mime_type = payload.get('type')

    try:
        content = payload['content']
    except KeyError:
        response = jsonify({
            'error': {
                'desc': 'no content has been supplied',
                'key': 'content',
                'code': 'MissingPayloadParameter',
            }
        })
        response.status_code = 400
        return response

    if mime_type is not None:
        if mime_type == 'application/json':
            content = json.loads(content)
        elif mime_type == 'application/octet-stream':
            content = pickle.loads(content)

    pipeline.extractor.put(content)

    response = Response()
    response.status_code = 202
    return response
