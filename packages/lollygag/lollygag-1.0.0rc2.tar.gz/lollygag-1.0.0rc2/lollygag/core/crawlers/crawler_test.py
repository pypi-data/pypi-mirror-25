import unittest
from lollygag.core.crawlers.crawler import Crawler
from lollygag.utility.test_utils import Any, CallableMock
from lollygag.dependency_injection.inject import Inject


class CrawlerTests(unittest.TestCase):
    def test_can_create(self):
        self.assertTrue(Crawler())
        self.assertTrue(Crawler("https://someuri"))

    def test_init(self):
        urls = ["https://fubar.com"]
        crawler = Crawler(urls[0])
        self.__assert_status(crawler.status, set(), set(urls), [])

    def __assert_status(self, status, visited_urls, urls_to_crawl, urls_in_progress):
        self.assertEqual(status.visited_urls, visited_urls)
        self.assertEqual(status.urls_to_crawl, urls_to_crawl)
        self.assertEqual(status.urls_in_progress, urls_in_progress)

    def test_initialize_status_no_protocol(self):
        crawler = Crawler()
        urls = ["winnie"]
        crawler.initialize_status(urls)
        self.assertEqual(crawler.protocol, "http://")

    def test_initialize_status_http(self):
        crawler = Crawler()
        urls = ["http://winnie"]
        crawler.initialize_status(urls)
        self.assertEqual(crawler.protocol, "http://")

    def test_initialize_status_https(self):
        crawler = Crawler()
        urls = ["https://winnie"]
        crawler.initialize_status(urls)
        self.assertEqual(crawler.protocol, "https://")

    def test_initialize_status_inits_status_correctly(self):
        crawler = Crawler()
        urls = ["http://a", "http://b", "http://c"]
        crawler.initialize_status(urls)
        self.__assert_status(crawler.status, set(), set(urls), [])


class Crawler_crawl_Tests(unittest.TestCase):

    def setUp(self):
        Inject.reset()
        Inject.register_feature('site_parser_factory', lambda: Any(parse=CallableMock()))
        Inject.register_feature('log_service',
                                Any(info=CallableMock(),
                                    error=CallableMock(),
                                    debug=CallableMock()))
        Inject.register_feature('work_service',
                                Any(request_work=CallableMock(callback=lambda cb: cb()),
                                    terminate_all=CallableMock(),
                                    active_count=CallableMock))

    def tearDown(self):
        Inject.reset()

    def test_crawl_calls_on_start(self):
        crawler = Crawler()
        callback = CallableMock()
        crawler.on_start(callback)
        crawler.crawl("foo")
        self.assertEqual(callback.call_count(), 1)

    def test_crawl_passes_crawljob_to_work_service(self):
        crawler = Crawler()
        crawler.crawl("bar")
        self.assertEqual(Inject.features['work_service'].request_work.call_count(), 1)
        job = Inject.features['work_service'].request_work.calls[0][0][0]
        self.assertTrue(callable(job))


if __name__ == '__main__':
    unittest.main()
