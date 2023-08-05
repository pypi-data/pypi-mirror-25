import unittest
from lollygag.core.single_site.link_crawler import LinkCrawler
from lollygag.dependency_injection.inject import Inject
from lollygag.utility.test_utils import Any

response = Any(text="", status_code=404, content="")
requests = Any(get=lambda x, **kw: response)
log_service = Any(info=lambda *a, **kw: None)

class CanCreateLinkCrawler(unittest.TestCase):
    def test_can_initialize(self):
        result = LinkCrawler()
        self.assertIsNot(result, None)

class LinkCrawlerCrawlTests(unittest.TestCase):
    def setUp(self):
        Inject.register_feature("requests", requests)
        Inject.register_feature("log_service", log_service)

    def tearDown(self):
        Inject.reset()

    def test_can_parse_empty(self):
        response.text = ""
        response.status_code = 200
        response.content = "Foobar"

        crawler = LinkCrawler()
        result = crawler.crawl("http://winnie.thepooh")

        self.assertTrue(result)
        self.assertEqual(result.link, "http://winnie.thepooh")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.page_size, 6)
        self.assertEqual(result.links, set())

    def test_can_find_links(self):
        response.text = '<a href="/tiggers"></a>'
        response.status_code = 200
        response.content = "Foobar"

        crawler = LinkCrawler()
        result = crawler.crawl("http://winnie.thepooh")

        self.assertTrue(result)
        self.assertEqual(result.link, "http://winnie.thepooh")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.page_size, 6)
        self.assertEqual(result.links, set(["/tiggers"]))

    def test_raises_on_None_url(self):
        crawler = LinkCrawler()
        with self.assertRaises(AssertionError):
            crawler.crawl(None)

if __name__ == '__main__':
    unittest.main()
