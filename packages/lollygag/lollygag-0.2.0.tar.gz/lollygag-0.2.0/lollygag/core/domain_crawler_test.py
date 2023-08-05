import unittest
from lollygag.core.domain_crawler import DomainCrawler
from lollygag.dependency_injection.inject import Inject
from lollygag.utility.test_utils import Any, CallableMock

crawl_result = Any(link="", status_code=200, page_size=0, links=[])
crawler = Any(crawl=CallableMock(returns=crawl_result))
site_crawler_factory = lambda: crawler
config = Any(threads=1, url=None, skip=[])
log = Any(write=CallableMock(), info=CallableMock(), error=CallableMock(), debug=CallableMock())
work_service = Any(request_work=CallableMock(), terminate_all=CallableMock(), active_count=CallableMock())

class DomainCrawlerTests(unittest.TestCase):
    def setUp(self):
        Inject.register_feature("site_crawler_factory", site_crawler_factory)
        Inject.register_feature("config_service", config)
        Inject.register_feature("log_service", log)
        Inject.register_feature("work_service", work_service)

    def tearDown(self):
        Inject.reset()
        crawler.crawl.reset()
        log.write.reset()           
        log.info.reset()           
        log.error.reset()           
        log.debug.reset()

class CanCreateDomainCrawler(DomainCrawlerTests):
    def test_can_initialize(self):
        result = DomainCrawler("http://winnie_the_pooh")
        self.assertIsNot(result, None)

class DomainCrawlerMethodTests(DomainCrawlerTests):
    start_mock = None
    callback = None

    def reset_threadmocks(self):
        self.callback = lambda *a, **kw: None
        self.start_mock = CallableMock(callback=lambda *a, **kw: self.callback())
        work_service.request_work.reset(callback=lambda cb: cb())
        work_service.active_count.reset(returns=0)

    def setUp(self):
        DomainCrawlerTests.setUp(self)
        self.crawler = DomainCrawler("http://winnie_the_pooh")
        crawler.crawl.reset(returns=crawl_result)
        self.reset_threadmocks()       

    def test_crawl_site_returns_the_crawl_result_from_crawler(self):
        self.crawler.status.urls_in_progress.append("http://winnie_the_pooh")
        result = self.crawler.crawl_site("http://winnie_the_pooh")
        self.assertTrue(result)
        self.assertEqual(result, crawl_result)

    def test_crawl_site_returns_none_on_interrupt(self):
        self.crawler.status.urls_in_progress.append("http://winnie_the_pooh")
        crawler.crawl.args["raises"] = KeyboardInterrupt() 
        with self.assertRaises(KeyboardInterrupt):
            result = self.crawler.crawl_site("http://winnie_the_pooh")
            self.assertEqual(result, None)

    def test_crawl_calls_crawler(self):
        self.crawler.crawl_domain()
        self.assertEqual(crawler.crawl.call_count(), 1)

    def test_crawls_all_links(self):
        crawl_result.links = ["http://winnie_the_pooh/kanga", "http://winnie_the_pooh/tiggers"]
        self.crawler.crawl_domain()
        self.assertEqual(crawler.crawl.call_count(), 3)

    def test_does_not_crawl_out_of_domain(self):
        crawl_result.links = ["http://kanga.com", "http://roo.com"]
        self.crawler.crawl_domain()
        self.assertEqual(crawler.crawl.call_count(), 1)

    def test_recognizes_domain(self):
        crawl_result.links = ["http://kanga.com", "http://roo.com", "http://www.winnie_the_pooh/tiggers", "http://winnie_the_pooh/tiggers"]
        self.crawler.crawl_domain()
        self.assertEqual(crawler.crawl.call_count(), 3)
   
    def test_recognizes_slashslash_domain(self):		
        crawl_result.links = ["//www.winnie_the_pooh/tiggers"]		
        self.crawler.crawl_domain()		
        self.assertEqual(crawler.crawl.call_count(), 2)


class DomainCrawlerNoUrlTests(DomainCrawlerTests):

    def test_can_create_with_no_url(self):
        DomainCrawler()
        
    def test_raises_AssertionError_if_no_url_is_present(self):
        crawler = DomainCrawler()
        with self.assertRaises(AssertionError):
            crawler.crawl_domain()

    def test_works_with_url_in_crawl(self):
        mycrawler = DomainCrawler()
        mycrawler.crawl_domain("www.winnie_the_pooh")
        self.assertEqual(crawler.crawl.call_count(), 1)

class EventTests(DomainCrawlerTests):
    def test_calls_callback_on_start(self):
        crawler = DomainCrawler()
        callback = CallableMock()
        crawler.on_start(callback)
        self.assertEqual(callback.call_count(), 0)
        crawler.crawl_domain("tiggers")
        self.assertEqual(callback.call_count(), 1)

    def test_calls_callback_on_finish(self):
        crawler = DomainCrawler()
        callback = CallableMock()
        crawler.on_finish(callback)
        self.assertEqual(callback.call_count(), 0)
        crawler.crawl_domain("tiggers")
        self.assertEqual(callback.call_count(), 1)

    def test_calls_callback_on_interrupt(self):
        crawler.crawl.args["raises"] = KeyboardInterrupt()
        myCrawler = DomainCrawler()
        callback = CallableMock()
        myCrawler.on_interrupt(callback)
        self.assertEqual(callback.call_count(), 0)
        with self.assertRaises(KeyboardInterrupt):
            myCrawler.crawl_domain("tiggers")
            self.assertEqual(callback.call_count(), 1)

    def test_on_interrupt_is_not_called_without_interrupt(self):
        myCrawler = DomainCrawler()
        callback = CallableMock()
        myCrawler.on_interrupt(callback)
        self.assertEqual(callback.call_count(), 0)
        myCrawler.crawl_domain("tiggers")
        self.assertEqual(callback.call_count(), 0)

if __name__ == '__main__':
    unittest.main()
