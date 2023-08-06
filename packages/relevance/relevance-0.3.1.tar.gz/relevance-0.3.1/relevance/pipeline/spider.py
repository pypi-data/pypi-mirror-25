"""
Relevance pipeline spider module.

This module provides an interface for ingesting content by crawling web pages.
"""

import typing
import logging
from queue import Queue
from scrapy import Spider
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from relevance.pipeline import Extractor


# Logging
logger = logging.getLogger('relevance.pipeline.spider')


class SpiderExtractor(Extractor):
    """
    Spider extractor.

    This classes wraps a scrapy spider into a pipeline extractor.
    """
    # The number of running instances
    __instances = Queue()

    def __init__(self, spider: Spider):
        """
        Initialize the extractor.

        :param spider: the spider object to use.
        """
        self.spider = spider
        self.queue = Queue()
        self.urls = set()

        def add_item(item, response, sender, spider, signal):
            if response.url not in self.urls:
                logger.info('spider extractor {0} extract item {1}: {2}'.format(
                    self, item, response,
                ))

                self.queue.put(item)
                self.urls.add(response.url)

        def start_spider():
            self.__instances.put(self)

        def stop_spider():
            self.__instances.get_nowait()
            if self.__instances.empty():
                reactor.stop()

        self.crawler = Crawler(spider)
        self.crawler.signals.connect(add_item, signals.item_scraped)
        self.crawler.signals.connect(start_spider, signals.spider_opened)
        self.crawler.signals.connect(stop_spider, signals.spider_closed)
        self.runner = CrawlerRunner()
        self.runner.crawl(self.crawler)

        logger.debug('initialize spider extractor {0}'.format(
            self,
        ))

        if reactor._stopped:
            reactor.run()

            logger.debug('spider extractor {0} starting reactor'.format(
                self,
            ))

    def get(self, timeout: int) -> object:
        """
        Get an item from the extractor.
        """
        return self.queue.get(timeout)

    def task_done(self):
        """
        Let the extractor know that an item was processed.
        """
        return self.queue.task_done()

    def get_status(self) -> dict:
        """
        Get additional state for the extractor.
        """
        return {
            'is_running': reactor._started,
            'size': self.queue.qsize(),
            'urls': self.spider.start_urls
        }


class SimpleSpiderExtractor(SpiderExtractor):
    """
    Simple spider extractor implementation.

    This classes automatically configures a spider extractor to extract data based
    on a certain mapping and follow URLs that match a certain selector.
    """
    def __init__(self, urls: typing.List[str], mapping: typing.Dict[str, str],
                 follow: typing.List[str]=None, match_urls: typing.List[str]=None):
        """
        Initialize the extractor.

        :param urls: the URLs to crawl.
        :param mapping: a dictionary mapping field names (keys) as scrapy selectors.
        :param follow: a list of selectors to check for links to follow.
        :param match_urls: a list of regular expressions to match against before following a
        link. If any matches, the link will be followed.
        """
        self.urls = urls
        self.mapping = mapping
        self.follow = follow or ['a']
        self.match_urls = match_urls or []

        class SimpleSpider(Spider):
            name = 'simplespider'
            start_urls = urls

            def parse(this, response):
                for selector in self.follow:
                    for next_page in response.css(selector):
                        href = next_page.css('::attr(href)')
                        found = False
                        for x in self.match_urls:
                            if href.re(x):
                                found = True

                        if found:
                            yield response.follow(next_page, this.parse)

                result = {}
                for field, selector in self.mapping.items():
                    result[field] = response.css(selector).extract()
                yield result

        super().__init__(SimpleSpider)
