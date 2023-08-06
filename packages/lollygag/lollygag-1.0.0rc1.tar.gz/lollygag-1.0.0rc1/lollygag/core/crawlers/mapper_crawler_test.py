import unittest
from lollygag.core.crawlers.domain_crawler_test import DomainCrawlerTests, parser as parser_mock
from lollygag.core.crawlers.mapper_crawler import MapperCrawler, get_all_nodes_in_tree
from lollygag.utility.test_utils import Any


class MapperCrawlerTests(DomainCrawlerTests):
    def setUp(self):
        super(MapperCrawlerTests, self).setUp()

    def tearDown(self):
        super(MapperCrawlerTests, self).tearDown()


class graph_tests(MapperCrawlerTests):

    def __test_graph_is_not_empty_crawl_result(self, mock):
        return lambda *a, **kw: {
            0: Any(link="winnie.the/pooh",
                   status_code=200,
                   page_size=0,
                   links=["./b"]),
            1: Any(link="winnie.the/b",
                   status_code=200,
                   page_size=0,
                   links=["./c"]),
            2: Any(link="winnie.the/b",
                   status_code=200,
                   page_size=0,
                   links=[])
        }[mock.call_count()]

    def test_graph_is_not_empty(self):
        parser_mock.parse.reset(callback=self.__test_graph_is_not_empty_crawl_result(parser_mock.parse))
        mapper = MapperCrawler()
        mapper.crawl("winnie.the/pooh")
        self.assertTrue(mapper.graph)
        self.assertEqual(len(mapper.graph), 2)

    def __test_graph_returns_all_paths_crawl_result(self, mock):
        def result(*a, **kw):
            try:
                return {
                    0: Any(link="winnie.the/pooh",
                           status_code=200,
                           page_size=0,
                           links=["./b"]),
                    1: Any(link="winnie.the/b",
                           status_code=200,
                           page_size=0,
                           links=["./c", "./d"]),
                }[mock.call_count()]
            except KeyError:
                return Any(link="winnie.the/Key", status_code=200, page_size=0, links=[])
        return result

    def test_graph_returns_all_paths(self):
        parser_mock.parse.reset(callback=self.__test_graph_returns_all_paths_crawl_result(parser_mock.parse))
        mapper = MapperCrawler()
        mapper.crawl("winnie.the/pooh")
        self.assertTrue(mapper.graph)
        self.assertEqual(len(mapper.graph), 3)
        print(mapper.graph)
        self.assertTrue(('http://winnie.the/pooh', 'http://winnie.the/b') in mapper.graph)
        self.assertTrue(('http://winnie.the/b', 'http://winnie.the/c') in mapper.graph)
        self.assertTrue(('http://winnie.the/b', 'http://winnie.the/d') in mapper.graph)


class get_all_nodes_in_tree_Tests(unittest.TestCase):
    def test_returns_all_nodes(self):
        tree = {
            'a': {
                'b': {
                    'c': None
                },
                'd': None
            }
        }
        result = get_all_nodes_in_tree(tree)
        self.assertEqual(result, ['a', 'b', 'c', 'd'])


if __name__ == '__main__':
    unittest.main()
