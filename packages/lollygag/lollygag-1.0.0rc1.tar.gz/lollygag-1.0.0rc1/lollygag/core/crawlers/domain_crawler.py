"""
Holds the DomainCrawler class.
"""
from lollygag.utility.url import get_domain
from lollygag.core.crawlers.crawler import Crawler


class DomainCrawler(Crawler):
    """
    A crawler that does not go outside the domain boundaries of the initial url
    """

    def __init__(self, url=None):
        self.domain = None
        super(DomainCrawler, self).__init__(url)

    def initialize_status(self, urls):
        """
        Extend the base initialize_status to store the domain being crawled.
        """
        self.domain = get_domain(urls[0])
        super(DomainCrawler, self).initialize_status(urls)

    def process_link(self, origin, link):
        """
        Extend the base process_link method to only return links that are on the same domain.
        """
        result = super(DomainCrawler, self).process_link(origin, link)
        if result is None or get_domain(result) != self.domain:
            return None
        return result

    def crawl(self, url=None):
        """
        Extend the base crawl method to assert if self.domain exists
        """
        if url:
            self.reset(url)
        assert self.domain, "Cannot start crawling without a domain!"
        super(DomainCrawler, self).crawl(url)
