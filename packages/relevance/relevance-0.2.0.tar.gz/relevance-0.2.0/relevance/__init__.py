"""
Content pipeline manager.

Relevance is a software suite that aims to address the common and recurring problem
of ingesting content, delivering it, searching it with relevant results and analyzing
its usage by the end-users, acting on the analytic data to provide the best results
possible.
"""

# Package version
__version__ = '0.2.0'


class Document(dict):
    """
    Document class.

    This class represents a document that can be searched for or indexed using an engine
    implementation.
    """
    def __init__(self, uid: object, doc_type: str):
        """
        Initialize the document.

        :param uid: the unique document identifier.
        :param doc_type: the document type, usually a table name or similar.
        """
        self.uid = uid
        self.doc_type = doc_type

    def __eq__(self, other):
        """
        Overload operator for comparison.
        """
        return dict(self) == dict(other) and self.uid == other.uid and \
            self.doc_type == other.doc_type
