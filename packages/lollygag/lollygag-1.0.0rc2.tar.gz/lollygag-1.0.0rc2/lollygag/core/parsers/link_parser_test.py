import unittest
from lollygag.core.parsers.link_parser import LinkParser
from lollygag.dependency_injection.inject import Inject
from lollygag.utility.test_utils import Any

response = Any(text="", status_code=404, content="")
requests = Any(get=lambda x, **kw: response)
log_service = Any(info=lambda *a, **kw: None, debug=lambda *a,
                  **kw: None, error=lambda *a, **kw: None, warn=lambda *a, **kw: None)


class CanCreateLinkCrawler(unittest.TestCase):
    def test_can_initialize(self):
        result = LinkParser()
        self.assertIsNot(result, None)


class LinkCrawlerCrawlTests(unittest.TestCase):
    def setUp(self):
        Inject.reset()
        Inject.register_feature("requests", requests)
        Inject.register_feature("log_service", log_service)

    def tearDown(self):
        Inject.reset()

    def test_can_parse_empty(self):
        response.text = ""
        response.status_code = 200
        response.content = "Foobar"

        crawler = LinkParser()
        result = crawler.parse("http://winnie.thepooh")

        self.assertTrue(result)
        self.assertEqual(result.link, "http://winnie.thepooh")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.page_size, 6)
        self.assertEqual(result.links, set())

    def test_can_find_links(self):
        response.text = '<a href="/tiggers"></a>'
        response.status_code = 200
        response.content = "Foobar"

        crawler = LinkParser()
        result = crawler.parse("http://winnie.thepooh")

        self.assertTrue(result)
        self.assertEqual(result.link, "http://winnie.thepooh")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.page_size, 6)
        self.assertEqual(result.links, set(["/tiggers"]))

    def test_raises_on_None_url(self):
        crawler = LinkParser()
        with self.assertRaises(AssertionError):
            crawler.parse(None)


if __name__ == '__main__':
    unittest.main()
