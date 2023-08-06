"""
Relevance engine core.

This package provides a unified interface for interacting with the different storage
and search backends.
"""

import abc

from relevance.query import Search
from relevance.mapping import Mapping
from relevance.document import Document
from relevance.document import ResultSet


class EngineError(Exception):
    """
    Exception class for engine error.

    This is the base exception class when an engine implementation encounters an
    error during a request.
    """
    pass


class MappingEngineError(EngineError):
    """
    Exception class for mapping engines.
    """
    pass


class SearchEngineError(EngineError):
    """
    Exception class for search engines.
    """
    pass


class MappingEngine(object, metaclass=abc.ABCMeta):
    """
    Abstract class for engines that support mapping.

    This class provides the interface for storage and search engines to support
    mapping definitions.
    """
    def __init__(self, target: str, **kwargs):
        """
        Initialize the engine.

        :param target: the storage engine target.
        """
        self.target = target

    @abc.abstractmethod
    def get_doc_types(self) -> list:
        """
        Get a list of available document types.

        :returns: a list of document type strings.
        """
        pass

    @abc.abstractmethod
    def get_mapping(self, doc_type: str) -> Mapping:
        """
        Get the mapping object for a specific document type.

        :param doc_type: the document type.
        :returns: the mapping object.
        """
        pass

    @abc.abstractmethod
    def put_mapping(self, doc_type: str, mapping: Mapping):
        """
        Update the mapping for a specific document type.

        :param doc_type: the document type.
        :param mapping: the mapping object.
        """
        pass


class SearchEngine(object, metaclass=abc.ABCMeta):
    """
    Search Engine abstract class.

    This class provides the abstract interface for storage engines to implement search
    functionality.
    """
    def __init__(self, target: str, *, facets: dict=None, auto_filters: bool=True, **kwargs):
        """
        Initialize the engine.

        :param target: the storage engine target.
        :param facets: a dictionary of facets definitions.
        :param auto_filters: whether to enable automatic filter definitions.
        """
        self.target = target
        self.facets = facets if facets is not None else {}
        self.auto_filters = auto_filters

    @abc.abstractmethod
    def search(self, search: Search) -> ResultSet:
        """
        Perform a search request on the engine.

        :param request: the request to execute.
        :returns: a result set object.
        """
        pass


class IngestionEngine(object, metaclass=abc.ABCMeta):
    """
    Ingestion Engine abstract class.

    This class provides the abstract interface for storage engines to implement indexing
    functionality.
    """
    def __init__(self, target: str, **kwargs):
        """
        Initialize the engine.

        :param target: the storage engine target.
        """
        self.target = target

    @abc.abstractmethod
    def publish(self, doc: Document) -> Document:
        """
        Index a document.

        :param doc: the document object to index.
        :returns: the updated, indexed document object.
        """
        pass

    @abc.abstractmethod
    def unpublish(self, schema: str, doc_type: str, uid: object):
        """
        Delete a document.

        :param schema: the document schema.
        :param doc_type: the document type.
        :param uid: the unique identifier for the document.
        """
        pass
