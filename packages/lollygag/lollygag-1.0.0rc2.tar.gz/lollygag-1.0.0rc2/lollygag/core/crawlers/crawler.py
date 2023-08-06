"""
Holds the Crawler class.
"""
import re
import time
from lollygag.core.crawlers.jobs.crawl_job import CrawlJob
from lollygag.dependency_injection.inject import Inject
from lollygag.dependency_injection.requirements import HasMethods, HasAttributes
from lollygag.utility.observer.subject import Subject
from lollygag.utility.url import get_protocol
from lollygag.utility.url import strip_beginning_slashes
from lollygag.utility.url import is_relative_link
from lollygag.utility.url import get_domain


class CrawlerStatus(object):
    """
    Represents the status of a crawl.
    """
    __slots__ = ["visited_urls", "urls_to_crawl", "urls_in_progress"]

    def __init__(self, *args):
        assert not args or len(args) == 4
        if args:
            self.reset(*args)

    def reset(self, visited_urls, urls_to_crawl, urls_in_progress):
        """
        Resets the instance's state.
        """
        self.visited_urls = visited_urls
        self.urls_to_crawl = urls_to_crawl
        self.urls_in_progress = urls_in_progress


class Crawler(object):
    """
    Crawls a resource starting from url
    Uses Crawlers created by site_parser_factory to crawl each resource,
    then decides the next pages to crawl based on the result

    Uses work_service to execute crawling jobs
    Uses log_service to display results and errors
    """
    site_parser_factory = Inject("site_parser_factory", return_factory=True)
    log_service = Inject("log_service", HasMethods("info", "error", "debug"))
    work_service = Inject("work_service",
                          HasMethods("request_work",
                                     "terminate_all", "active_count"),
                          cache=True)
    config_service = Inject("config_service", HasAttributes("skip"))

    def __init__(self, urls=None):
        self.on_start = Subject()
        self.on_interrupt = Subject()
        self.on_finish = Subject()
        self.protocol = None
        self.status = CrawlerStatus()
        self.reset(urls)

    def reset(self, url):
        """
        Reset the crawler's state
        """
        self.status.reset(set(), set(), [])
        if not url:
            return
        if not isinstance(url, list):
            url = [url]
        self.initialize_status(url)

    def initialize_status(self, urls):
        """
        Initialize the crawler's status field by a collection of urls
        """
        self.protocol = get_protocol(urls[0])
        if not self.protocol:
            self.protocol = "http://"
            urls[0] = "%s%s" % (self.protocol, urls[0])
        self.status.urls_to_crawl.add(urls[0])
        for url in urls[1:]:
            processed = self.process_link(None, url)
            if not processed:
                raise AttributeError(
                    "Url=[%s] is not valid in this collection!" % url)
            self.status.urls_to_crawl.add(processed)

    def crawl(self, url=None):
        """
        Starts the crawl procedure
        Returns when the crawling is complete
        or a KeyboardInterrupt or SystemExit is raised
        Terminates remaining work if interrupted
        """
        if url:
            self.reset(url)
        self.log_service.info(
            "----------Crawl starting from url=[{url}]----------".format(
                url=url)
        )
        self.on_start.next(url)
        self.__request_crawl_work()
        try:
            while self.is_task_left():
                self.__sleep_until_task_is_available()
                self.__request_crawl_work()
        except (KeyboardInterrupt, SystemExit) as error:
            self.handle_interrupt(error)
        finally:
            self.handle_crawl_finish()

    def __sleep_until_task_is_available(self):
        if not self.is_waiting_for_url():
            return
        self.log_service.debug("No urls to crawl, going to sleep.",
                               "Work in progress=[%s]" %
                               self.work_service.active_count())
        while self.is_waiting_for_url():
            time.sleep(1)

    def __request_crawl_work(self):
        return self.work_service.request_work(CrawlJob(self))

    def process_links(self, origin, links):
        """
        Process a collection of links found at origin
        """
        result = []
        for link in links:
            processed_link = self.process_link(origin, link)
            if self.is_new_link(processed_link):
                result.append(processed_link)
                self.status.urls_to_crawl.add(processed_link)
        return result

    def is_new_link(self, link):
        """
        Returns if the link has been seen by the crawler before
        """
        return link \
            and link not in self.status.visited_urls \
            and link not in self.status.urls_to_crawl

    def process_link(self, origin, link):
        """
        Processes a newly found link
        For relative links the origin link will be used as base
        """
        if not link or any([x for x in self.config_service.skip if re.search(x, link.lower())]):
            return None
        if is_relative_link(link):
            if link[0] == ".":
                link = link[1::]
            link = "%s%s%s" % (self.protocol, get_domain(origin), link)
        link = strip_beginning_slashes(link)
        if not get_protocol(link):
            link = "%s%s" % (self.protocol, link)
        return link

    def get_status_message(self):
        """
        Returns a message about the current progress
        """
        visited = len(self.status.visited_urls)
        in_progess = len(self.status.urls_in_progress)
        todo = len(self.status.urls_to_crawl)
        message = """--------------------Crawl status--------------------
                                        Urls visited=[%s]
                                        Urls in progess=[%s]
                                        Urls left=[%s]""" %\
            (visited, in_progess, todo)
        return message

    def is_waiting_for_url(self):
        """
        Returns if urls_to_crawl is empty, but there are urls is progress
        """
        return not any(self.status.urls_to_crawl) \
            and any(self.status.urls_in_progress)

    def is_task_left(self):
        """
        Returns if there are any urls that haven't been processed yet
        """
        return any(self.status.urls_in_progress + list(self.status.urls_to_crawl))

    def handle_interrupt(self, error):
        """
        Handles crawling interruptions
        Calls on_interrupt obeservers
        Terminates pending jobs
        """
        self.log_service.info(
            "----------Crawling was interrupted----------", error)
        self.on_interrupt.next()
        self.work_service.terminate_all()

    def handle_crawl_finish(self):
        """
        Handles crawling finish
        Calls on_finish observers
        Logs the final status
        """
        self.on_finish.next(self.status.visited_urls,
                            self.status.urls_in_progress,
                            self.status.urls_to_crawl)
        self.log_service.info(self.get_status_message())
        self.log_service.info("----------Crawl finished----------\n")
