import re
import time
import requests
from lollygag.utility.url import get_protocol
from lollygag.utility.url import strip_beginning_slashes
from lollygag.utility.url import get_domain
from lollygag.utility.url import is_relative_link
from lollygag.dependency_injection.inject import Inject
from lollygag.dependency_injection.requirements import HasMethods, HasAttributes
from lollygag.utility.observer.subject import Subject

class DomainCrawlerStatus(object):
    __slots__ = ["domain", "visited_urls", "urls_to_crawl", "urls_in_progress"]

    def __init__(self, *args):
        assert not args or len(args) == 4
        if args:
            self.reset(*args)

    def reset(self, domain, visited_urls, urls_to_crawl, urls_in_progress):
        self.domain = domain
        self.visited_urls = visited_urls
        self.urls_to_crawl = urls_to_crawl
        self.urls_in_progress = urls_in_progress

class DomainCrawler(object):
    """
    Crawls a resource starting from url
    Uses Crawlers created by site_crawler_factory to crawl each resource,
    then decides the next pages to crawl based on the result
    Does not go outside the domain boundaries of the initial url

    Uses work_service to execute crawling jobs
    Uses log_service to display results and errors
    """
    site_crawler_factory = Inject("site_crawler_factory", return_factory=True)
    log_service = Inject("log_service", HasMethods("info", "error", "debug"))
    work_service = Inject("work_service", \
                        HasMethods("request_work", "terminate_all", "active_count"))
    config_service = Inject("config_service", HasAttributes("url"))

    def __init__(self, url=None):
        self.on_start = Subject()
        self.on_interrupt = Subject()
        self.on_finish = Subject()
        self.status = DomainCrawlerStatus()
        if not url:
            url = self.config_service.url
        self.reset(url)

    def reset(self, url):
        self.status.reset(None, set(), [], [])
        if not url:
            return
        self.protocol = get_protocol(url)
        if not self.protocol:
            self.protocol = "http://"
            url = "%s%s" % (self.protocol, url)
        self.status.domain = get_domain(url)
        self.status.urls_to_crawl.append(url)

    def crawl_domain(self, url=None):
        """
        Starts the crawl procedure
        Returns when the crawling is complete or a KeyboardInterrupt or SystemExit is raised
        Terminates remaining work if interrupted
        """
        if url:
            self.reset(url)
        assert self.status.domain, "Cannot start crawling without a URL!"
        self.log_service.info("----------Crawl starting----------")
        self.on_start.next(url)
        self.__request_crawl_job()
        try:
            while self.is_task_left():
                self._run()
        except (KeyboardInterrupt, SystemExit) as error:
            self.handle_interrupt(error)
        finally:
            self.handle_crawl_finish()

    def handle_interrupt(self, error):
        self.log_service.info("----------Crawling was interrupted----------", error)
        self.on_interrupt.next()
        self.work_service.terminate_all()

    def handle_crawl_finish(self):
        self.on_finish.next(self.status.visited_urls,
                            self.status.urls_in_progress,
                            self.status.urls_to_crawl)
        self.log_service.info(self.get_status_message())
        self.log_service.info("----------Crawl finished----------\n")

    def get_status_message(self):
        visited = len(self.status.visited_urls)
        in_progess = len(self.status.urls_in_progress)
        todo = len(self.status.urls_to_crawl)
        message = """--------------------Crawl status--------------------
                                        Urls visited=[%s]
                                        Urls in progess=[%s]
                                        Urls left=[%s]""" % (visited, in_progess, todo)
        return message

    def _run(self):
        self.__sleep_until_task_is_available()
        self.__request_crawl_job()

    def __sleep_until_task_is_available(self):
        if not self.is_waiting_for_url():
            return
        self.log_service.debug("No urls to crawl, going to sleep."\
                             , "Work in progress=[%s]" % self.work_service.active_count())
        while self.is_waiting_for_url():
            time.sleep(1)

    def is_waiting_for_url(self):
        return not any(self.status.urls_to_crawl) \
               and self.work_service.active_count()

    def is_task_left(self):
        return any(self.status.urls_in_progress + self.status.urls_to_crawl)

    def __request_crawl_job(self):
        return self.work_service.request_work(self.__crawl_urls)

    def __crawl_urls(self):
        crawler = self.site_crawler_factory()
        while self.status.urls_to_crawl:
            self.__run_crawl(crawler)

    def __run_crawl(self, crawler=None):
        try:
            url = self.status.urls_to_crawl.pop()
        except IndexError:
            return
        self.status.urls_in_progress.append(url)
        result = self.crawl_site(url, crawler)
        self.status.visited_urls.add(url)
        if result:
            self.process_links(url, result.links)
        self.log_service.debug(self.get_status_message())

    def crawl_site(self, url, crawler=None):
        """
        Crawls the given url using a crawler made by site_crawler_factory
        If a requests.exceptions.ConnectionError or requests.exceptions.SSLError is raised
        returns None
        """
        try:
            crawler = self.site_crawler_factory() if crawler is None else crawler
            result = crawler.crawl(url)
            return result
        except (requests.exceptions.ConnectionError, requests.exceptions.SSLError) as error:
            self.log_service.error("Error while crawling site=[%s]" % url, str(error))
            return None
        finally:
            self.status.urls_in_progress.remove(url)

    def process_links(self, origin, links):
        #pylint: disable=unused-argument
        result = []
        for link in links:
            processed_link = self.process_link(link)
            if self.is_new_link(processed_link):
                result.append(processed_link)
                self.status.urls_to_crawl.append(processed_link)
        return result

    def is_new_link(self, link):
        return link \
               and link not in self.status.visited_urls \
               and link not in self.status.urls_to_crawl

    def process_link(self, link):
        if not link or any(filter(lambda x: re.search(x, link.lower()), self.config_service.skip)):
            return None
        if is_relative_link(link):
            if link[0] == ".":
                link = link[1::]
            link = "%s%s" % (self.status.domain, link)
        link = strip_beginning_slashes(link)
        if get_domain(link) != self.status.domain:
            return None
        if not get_protocol(link):
            link = "%s%s" % (self.protocol, link)
        return link
