"""
Relevance pipeline REST module.

This module provides an interface for dealing with queues via an API.
"""

import json
import pickle
import typing
from flask import request
from flask import jsonify
from flask import Response
from queue import Queue
from queue import Empty
from werkzeug import exceptions

from relevance.pipeline import EmptyError
from relevance.pipeline import Extractor
from relevance.api.pipelines import app
from relevance.api.pipelines import PipelineNotFoundError


class QueueExtractor(Queue, Extractor):
    """
    Queue extractor.

    This class provides an extractor that wraps a queue that can be populated via
    an API.
    """
    def get(self, *args, **kwargs) -> object:
        """
        Get an item from the extractor.

        :raises: EmptyError: if the queue is empty.
        """
        try:
            return super().get(*args, **kwargs)
        except Empty:
            raise EmptyError()

    def get_status(self) -> typing.Dict[str, object]:
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

    :returns: a 202 response on success.
    """
    try:
        pipeline = app.data.pipelines[pipeline_name]
    except KeyError:
        raise PipelineNotFoundError(pipeline_name)

    if not isinstance(pipeline, QueueExtractor):
        raise exceptions.MethodNotAllowed()

    payload = request.get_json()
    mime_type = payload.get('type')

    try:
        content = payload['content']
    except KeyError as e:
        raise MissingParameterError(str(e))

    if mime_type is not None:
        if mime_type == 'application/json':
            content = json.loads(content)
        elif mime_type == 'application/octet-stream':
            content = pickle.loads(content)
        else:
            raise DocumentTypeError(mime_type)

    pipeline.extractor.put(content)

    response = Response()
    response.status_code = 202
    return response


class DocumentTypeError(exceptions.UnprocessableEntity):
    """
    Exception raised when a document type cannot be decoded.
    """
    pass


@app.errorhandler(DocumentTypeError)
def document_type_error(e: DocumentTypeError) -> Response:
    response = jsonify({
        'error': {
            'desc': 'the supplied document type cannot be decoded',
            'key': str(e),
            'code': e.__class__.__name__,
        }
    })
    response.status_code = 501
    return response


class MissingParameterError(exceptions.BadRequest):
    """
    Exception raised when a parameter is missing from the payload.
    """
    pass


@app.errorhandler(MissingParameterError)
def missing_param_error(e: MissingParameterError) -> Response:
    response = jsonify({
        'error': {
            'desc': 'the payload is missing a required parameter',
            'key': str(e),
            'code': e.__class__.__name__,
        }
    })
    response.status_code = 501
    return response
