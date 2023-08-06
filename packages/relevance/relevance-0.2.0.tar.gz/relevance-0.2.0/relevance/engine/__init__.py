"""
Relevance engine core.

This package provides a unified interface for interacting with the different storage
and search backends.
"""

import abc
import datetime

from relevance import Document
from relevance.query import Search
from relevance.mapping import Mapping


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


class SearchRuntimeError(SearchEngineError, RuntimeError):
    """
    Exception class when the search triggers an error at runtime.
    """
    pass


class MappingEngine(object, metaclass=abc.ABCMeta):
    """
    Abstract class for engines that support mapping.

    This class provides the interface for storage and search engines to support
    mapping definitions.
    """
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
    def __init__(self, target: str, *, facets: dict=None, auto_filters: bool=True):
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
    def search(self, search: Search) -> 'ResultSet':
        """
        Perform a search request on the engine.

        :param request: the request to execute.
        :returns: a result set object.
        """
        pass


class Result(Document):
    """
    Result class.

    This class provides the interface for handling single search results.
    """
    def __init__(self, *args, score: float):
        """
        Initialize the result.

        :param score: the relevancy score.
        """
        super().__init__(*args)
        self.score = score


class ResultSet(list):
    """
    Result set class.

    This class provides the interface for handling search result lists.
    """
    def __init__(self, search: Search, engine: SearchEngine):
        """
        Initialize the result set.

        :param search: the search object.
        :param engine: the engine object.
        """
        self.search = search
        self.engine = engine
        self.time_start = datetime.datetime.now()
        self.time_end = None
        self.facets = None
        self.count = 0

    @property
    def time(self) -> float:
        """
        Get the total amount of time the request took.
        """
        return (self.time_end - self.time_start).total_seconds()
