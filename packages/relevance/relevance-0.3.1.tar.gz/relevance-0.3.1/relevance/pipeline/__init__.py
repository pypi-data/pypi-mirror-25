"""
Relevance ingestion pipeline.

This package provides the classes and interfaces for ingesting content using the
engine abstraction layer.
"""

import abc
import typing
import logging
import threading

from relevance.document import Document


# Logging
logger = logging.getLogger('relevance.pipeline')


class EmptyError(IOError):
    """
    Exception raised when an extractor encounters an error.
    """
    pass


class Extractor(object, metaclass=abc.ABCMeta):
    """
    Extractor abstract class.

    An extractor's responsibility is to pull raw content into the pipeline for
    further processing.
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
    def get_status(self) -> typing.Dict[str, object]:
        """
        Get additional state for the extractor.
        """
        pass


class Publisher(object):
    """
    Publisher class.

    A publisher is an object that takes processed content and publishes to
    a data engine.
    """
    def __init__(self, func: typing.Callable):
        """
        Initialize the publisher.

        :param func: a function to call when publishing.
        """
        self.func = func
        self.publish_count = 0
        self.error_count = 0

        logger.debug('initialize publisher {0} with {1}'.format(
            self, self.func,
        ))

    def publish(self, content: object) -> object:
        """
        Publish a data item.

        :param content: the content to publish.
        :returns: returns a status item.
        """
        try:
            result = self.func(content)
            self.publish_count += 1
            logger.info('publisher {0} item published: {1}'.format(
                self, content,
            ))
            return result
        except Exception as e:
            self.error_count += 1
            logger.error('publisher {0} item error: {1}'.format(
                self, e,
            ))
            raise

    def get_status(self) -> typing.Dict[str, object]:
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

    This class wraps around an existing extractor and converts the input dictionary into a
    document object.
    """
    def __init__(self, handler: Extractor, schema: str=None, doc_type: str=None):
        """
        Initialize the extractor.

        :param handler: the actual extractor handler to launch after the document is converted.
        :param schema: the name of the schema to apply to the resulting document.
        :param doc_type: the document type to apply to the resulting document.
        """
        self.handler = handler
        self.schema = schema
        self.doc_type = doc_type

        logger.debug('initialize document extractor {0} with {1} to {2} as {3}'.format(
            self, self.handler, self.schema, self.doc_type,
        ))

    def get(self, timeout: int) -> object:
        """
        Get an item from the extractor.

        :raises: KeyError: when a required payload element is missing.
        """
        item = self.handler.get(timeout)

        try:
            schema = self.schema if self.schema is not None else item['_schema']
            doc_type = self.doc_type if self.doc_type is not None else item['_type']
            uid = item.get('_uid', None)
        except KeyError as e:
            raise KeyError('missing payload item {0}'.format(str(e)))

        doc = Document(schema, doc_type, uid)
        doc.update(item)

        return doc

    def task_done(self):
        """
        Let the extractor know that an item was processed.
        """
        return self.handler.task_done()

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

        logger.debug('initialize pipeline {0}, ext={1}, pub={2}, func={3}'.format(
            self, self.extractor, self.publisher, self.funcs,
        ))

    def run(self, timeout: int=None) -> object:
        """
        Run an item from the extractor.

        :param timeout: a timeout to wait before an item becomes available.
        :returns: the processed item.
        """
        try:
            item = self.extractor.get(timeout=timeout)
        except EmptyError as e:
            raise

        logger.debug('pipeline {0} extracted item: {1}'.format(
            self, item,
        ))

        try:
            for func, desc in self.funcs:
                logger.debug('pipeline {0} applying {1} ({2}): {3}'.format(
                    self, func, desc, item,
                ))

                item = func(item)

            logger.debug('pipeline {0} publishing: {1}'.format(
                self, item,
            ))

            return self.publisher(item)
        finally:
            self.extractor.task_done()
            logger.debug('pipeline {0} release item'.format(
                self,
            ))


class ThreadedPipeline(Pipeline):
    """
    Threaded pipeline class.

    A pipeline variant that runs in a separate thread.
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

        :param timeout: the amount of time, in seconds, to wait for the extractor at
        in the event loop.
        """
        if self.thread is not None:
            logger.warn('threaded pipeline {0} already started'.format(
                self,
            ))
            return

        def run_thread():
            logger.debug('threaded pipeline {0} thread starting'.format(
                self,
            ))

            while True:
                try:
                    result = self.run(timeout=timeout)
                    logger.info('threaded pipeline {0} item processed: {1}'.format(
                        self, result,
                    ))
                except EmptyError:
                    if not self.is_started:
                        break
                except StopIteration as e:
                    logger.info('threaded pipeline {0} skip item: {1}'.format(
                        self, e,
                    ))
                except Exception as e:
                    logger.error('threaded pipeline {0} item error: {1}'.format(
                        self, e,
                    ))

            logger.debug('threaded pipeline {0} thread ending'.format(
                self,
            ))

        self.is_started = True
        self.thread = threading.Thread(target=run_thread)
        self.thread.start()

        logger.info('threaded pipeline {0} starting {1}'.format(
            self, self.thread,
        ))

    def stop(self):
        """
        Stop the pipeline thread.
        """
        if self.thread is None:
            logger.warn('threaded pipeline {0} already stopped'.format(
                self,
            ))
            return

        self.is_started = False
        self.thread.join()

        logger.info('threaded pipeline {0} joined'.format(
            self,
        ))
