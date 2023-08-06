"""
Relevance ingestion pipeline.

This package provides the classes and interfaces for ingesting content using the
engine abstraction layer.
"""

import abc
import threading

from relevance.document import Document


class ExtractorError(Exception):
    """
    Exception raised when an extractor cannot feed a new item.
    """
    pass


class Extractor(object, metaclass=abc.ABCMeta):
    """
    Extractor protocol class.

    An extractor is a class that implements this protocol, such as the queue classes
    found in the queue module. Extractors should be thread safe.
    """
    @abc.abstractmethod
    def get(self, timeout: int) -> object:
        """
        Get an item from the extractor.

        :param timeout: a timeout, in seconds after which an exception is raised
        if an item cannot be retrieved.
        :returns: the retrieved item.
        """
        pass

    @abc.abstractmethod
    def task_done(self):
        """
        Let the extractor know that an item was processed.

        This method is called after each item is processed.
        """
        pass

    @abc.abstractproperty
    def get_status(self) -> dict:
        """
        Get additional state for the extractor.
        """
        pass


class Publisher(object):
    """
    Publisher class.
    """
    def __init__(self, func):
        """
        Initialize the publisher.

        :param func: a function to call when publishing.
        """
        self.func = func
        self.publish_count = 0
        self.error_count = 0

    def publish(self, content: object) -> object:
        """
        Publish a data item.

        :param content: the content to publish.
        :returns: returns a status item.
        """
        try:
            result = self.func(content)
            self.publish_count += 1
            return result
        except Exception as e:
            self.error_count += 1
            raise

    def get_status(self) -> dict:
        """
        Get additional state for the publisher.
        """
        return {
            'publish_count': self.publish_count,
            'error_count': self.error_count,
        }


class DocumentExtractor(Extractor):
    """
    Extracts a dictionary payload into a document.

    This class wraps around an existing extractor and converts a dictionary into a
    document object.
    """
    def __init__(self, handler: Extractor, schema: str=None, doc_type: str=None):
        """
        Initialize the extractor.

        :param handler: the actual extractor handler after the document is converted.
        :param schema: the document schema to apply.
        :param doc_type: the document type to apply.
        """
        self.handler = handler
        self.schema = schema
        self.doc_type = doc_type

    def get(self, timeout: int) -> object:
        """
        Get an item from the extractor.
        """
        item = self.handler.get(timeout)

        try:
            schema = self.schema if self.schema is not None else item['_schema']
            doc_type = self.doc_type if self.doc_type is not None else item['_type']
            uid = item.get('_uid', None)
        except KeyError as e:
            raise ExtractorError('missing payload item {0}'.format(str(e)))

        doc = Document(schema, doc_type, uid)
        doc.update(item)

        return doc

    def task_done(self):
        """
        Let the extractor know that an item was processed.
        """
        return self.handler.task_done()

    def qsize(self) -> int:
        """
        Get the size of the queue.
        """
        return self.handler.qsize()

    def __getattr__(self, name: str) -> object:
        """
        Overload get attribute method.
        """
        return getattr(self.handler, name)


class Pipeline(object):
    """
    Ingestion pipeline class.

    The class encapsulates an extractor and a list of callables to execute for each
    input item.
    """
    def __init__(self, extractor: Extractor, publisher: Publisher, *args):
        """
        Initialize the pipeline.

        :param extractor: a extractor object containing the input data.
        :param publisher: a publisher object to send the output data.
        :param args: a list of tuples or callables to add to the pipeline.
        """
        self.extractor = extractor
        self.publisher = publisher
        self.funcs = []

        for x in args:
            if isinstance(x, tuple):
                self.funcs.append(x[0], x[1])
            else:
                self.funcs.append((x, None))

    def run(self, timeout: int=None):
        """
        Run an item from the extractor.

        :param timeout: a timeout to wait before an item becomes available.
        :returns: the processed item.
        :raises: a StopIteration exception is the item must be skipped.
        """
        try:
            item = self.extractor.get(timeout=timeout)
        except Exception as e:
            raise ExtractorError(e)

        for func, desc in self.funcs:
            item = func(item)

        self.extractor.task_done()
        return self.publisher(item)


class ThreadedPipeline(Pipeline):
    """
    Threaded pipeline class.

    A pipeline variant that runs in a thread.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the pipeline.
        """
        super().__init__(*args, **kwargs)
        self.thread = None
        self.is_started = False

    def start(self, timeout: float=1):
        """
        Start the pipeline thread.

        :param timeout: the amount of time, in seconds, to wait for the extractor.
        """
        if self.thread is not None:
            return

        def run_thread():
            while True:
                try:
                    self.run(timeout=timeout)
                except ExtractorError:
                    if not self.is_started:
                        break
                except StopIteration:
                    pass
                except Exception:
                    raise

        self.is_started = True
        self.thread = threading.Thread(target=run_thread)
        self.thread.start()

    def stop(self):
        """
        Stop the pipeline thread.
        """
        if self.thread is None:
            return

        self.is_started = False
        self.thread.join()
