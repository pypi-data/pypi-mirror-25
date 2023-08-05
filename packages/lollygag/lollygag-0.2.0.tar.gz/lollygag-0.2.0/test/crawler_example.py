#!/usr/bin/python

from lollygag import run
from lollygag.services import register_services
from lollygag.services import Services
from lollygag.core.single_site.link_crawler import LinkCrawler
from lollygag.core.domain_crawler import DomainCrawler

class MyCrawler(LinkCrawler):
    """
    This is a custom crawler to handle a single webpage
    If you wish to preserve existing functionality when overriding methods,
    do not forget to call the super method aswell
    """
    def feed(self, data):
        # Override the feed method to customize handling the whole page data
        self.log_service.info("Yeah boi, a page!")
        return LinkCrawler.feed(self, data)

    def handle_starttag(self, tag, attrs):
        """
        Override HTMLParser methods for custom behaviour
        Call the super method to return links on the page
        The default DomainCrawler class will continue crawling if crawl() returns a 
        CrawlResult with links
        """
        super(MyCrawler, self).handle_starttag(tag, attrs)
        if(tag == 'img'):
            self.log_service.info("Yeeeeaaaah boiiiiiii, I found an %s" % (tag))
        if(tag == 'a'):
            self.log_service.debug("Boi, I found a link!")

def on_finish(log_service):
    def callback(*args):
        log_service.info("-------------Yeah boiiii, done-----------------")
    return callback

def main():
    # Override site_crawler_factory with my own implementation
    Services.site_crawler_factory = MyCrawler
    register_services()
    crawler = DomainCrawler()
    crawler.on_finish(on_finish(Services.log_service()))
    run(crawler=crawler)

if __name__ == '__main__':
    main()
