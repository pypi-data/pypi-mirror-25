import unittest
from lollygag.core.crawlers.jobs.crawl_job import CrawlJob
from lollygag.utility.test_utils import Any, CallableMock
from lollygag.dependency_injection.inject import Inject
from requests.exceptions import ConnectionError as ConnectionError


class CrawlJobTests(unittest.TestCase):

    def setUp(self):
        self.log_service = Any(debug=CallableMock(), error=CallableMock())
        self.crawl_result = Any(link="", status_code=200, page_size=0, links=[])
        self.parser = Any(parse=CallableMock(returns=self.crawl_result))
        self.crawler = Any(status=Any(urls_in_progress=[], urls_to_crawl=[], visited_urls=set()),
                           site_parser_factory=CallableMock(returns=self.parser),
                           process_links=CallableMock(),
                           get_status_message=CallableMock())
        Inject.reset()
        Inject.register_feature('log_service', self.log_service)

    def tearDown(self):
        Inject.reset()

    def test_crawl_site_returns_the_crawl_result_from_crawler(self):
        self.crawler.status.urls_in_progress.append("http://winnie_the_pooh")
        job = CrawlJob(self.crawler)
        result = job.crawl_site("http://winnie_the_pooh")
        self.assertTrue(result)
        self.assertEqual(result, self.crawl_result)

    def test_crawl_site_returns_none_on_interrupt(self):
        self.crawler.status.urls_in_progress.append("http://winnie_the_pooh")
        self.parser.parse.raises(ConnectionError())
        result = "something that's not None"
        job = CrawlJob(self.crawler)
        result = job.crawl_site("http://winnie_the_pooh")
        self.assertEqual(result, None)
        self.assertEqual(self.log_service.error.call_count(), 1, "Logs the error")

    def test_crawl_site_removes_url_on_finish(self):
        self.crawler.status.urls_in_progress.append("http://winnie_the_pooh")
        self.parser.parse.raises(ConnectionError())
        job = CrawlJob(self.crawler)
        job.crawl_site("http://winnie_the_pooh")
        self.assertEqual(self.crawler.status.urls_in_progress, [])
        self.crawler.status.urls_in_progress.append("http://winnie_the_pooh")
        self.parser.parse.returns(self.crawl_result)
        job = CrawlJob(self.crawler)
        job.crawl_site("http://winnie_the_pooh")
        self.assertEqual(self.crawler.status.urls_in_progress, [])

    def test_does_not_raise_if_the_url_is_removed_before_parse_finish(self):
        self.crawler.status.urls_in_progress = []
        self.parser.parse.returns(self.crawl_result)
        job = CrawlJob(self.crawler)
        job.crawl_site("http://winnie_the_pooh")

    def test_uses_the_parser_to_parse_by_the_url(self):
        self.parser.parse.returns(self.crawl_result)
        job = CrawlJob(self.crawler)
        job.crawl_site("http://winnie_the_pooh")
        self.assertEqual(self.parser.parse.call_count(), 1)
        self.assertEqual(self.parser.parse.calls[0][0][0], "http://winnie_the_pooh")

    def test_prints_status_on_every_crawl(self):
        self.crawler.status.urls_to_crawl = ["http://winnie_the_pooh", "http://kanga_the_mommy"]
        job = CrawlJob(self.crawler)
        job.run()
        self.assertEqual(self.log_service.debug.call_count(), 2)

    def test_parses_links_using_the_crawler(self):
        urls = ["http://winnie_the_pooh", "http://kanga_the_mommy"]
        self.crawler.status.urls_to_crawl = list(map(lambda x: x, urls))
        self.crawl_result.links = ['a', 'b']
        job = CrawlJob(self.crawler)
        job.run()
        self.assertEqual(self.crawler.process_links.call_count(), 2)
        self.assertEqual(self.crawler.process_links.calls[0][0], (urls[1], self.crawl_result.links))
        self.assertEqual(self.crawler.process_links.calls[1][0], (urls[0], self.crawl_result.links))

    def test_moves_crawler_status(self):
        urls = ["http://winnie_the_pooh", "http://kanga_the_mommy"]
        self.crawler.status.urls_to_crawl = list(map(lambda x: x, urls))
        job = CrawlJob(self.crawler)
        self.assertEqual(self.crawler.status.urls_in_progress, [])
        self.assertEqual(self.crawler.status.urls_to_crawl, urls)
        self.assertEqual(self.crawler.status.visited_urls, set())
        job.run()
        self.assertEqual(self.crawler.status.urls_in_progress, [])
        self.assertEqual(self.crawler.status.urls_to_crawl, [])
        self.assertEqual(self.crawler.status.visited_urls, set(urls))


if __name__ == '__main__':
    unittest.main()
