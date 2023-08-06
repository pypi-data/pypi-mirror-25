"""
Relevance document module.

This module provides the interface for representing documents, search results, and
result sets.
"""

import datetime


class Document(dict):
    """
    Document class.

    This class represents a document that can be searched for or indexed using an engine
    implementation.
    """
    def __init__(self, schema: str, doc_type: str, uid: object):
        """
        Initialize the document.

        :param schema: the document schema.
        :param doc_type: the document type, usually a table name or similar.
        :param uid: the unique document identifier.
        """
        self.schema = schema
        self.doc_type = doc_type
        self.uid = uid

    def __eq__(self, other):
        """
        Overload operator for comparison.
        """
        return dict(self) == dict(other) and self.uid == other.uid and \
            self.doc_type == other.doc_type


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
    def __init__(self):
        """
        Initialize the result set.

        :param search: the search object.
        :param engine: the engine object.
        """
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
