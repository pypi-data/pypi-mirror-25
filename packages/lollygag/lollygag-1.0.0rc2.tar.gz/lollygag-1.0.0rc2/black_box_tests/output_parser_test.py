from black_box_tests import parse_crawler_output
import unittest

OUTPUT = """[Debug]Thread=[WSc[0]--2]        No urls to crawl, going to sleep. Work in progress=[1]
[Error]Thread=[WSc[2]--21]       Error while crawling site=[http://kanga.pooh] HTTPConnectionPool(host='kanga.pooh', port=80)
[Info]Thread=[WSc[1]--20]        Link=[https://snorrwe.github.io/crawler_test/] StatusCode=[200] Size=[404]
"""


class OutputParserTests(object):

    def setUp(self):
        self.result = parse_crawler_output(OUTPUT, "No urls to crawl, going to sleep")

    def test_can_parse_results(self):
        self.assertEqual([("https://snorrwe.github.io/crawler_test/", 200, 404)], result['results'])

    def test_can_parse_errors(self):
        self.assertEqual(
            ["Error while crawling site=[http://kanga.pooh] HTTPConnectionPool(host='kanga.pooh', port=80)"], result['errors'])

    def test_can_parse_custom(self):
        self.assertEqual(
            ["[Debug]Thread=[WSc[0]--2]        No urls to crawl, going to sleep. Work in progress=[1]\n"], result['custom'])


if __name__ == '__main__':
    main()
