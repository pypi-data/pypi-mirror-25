#!/usr/bin/python

from unittest import TestCase, main as unittest_main
import subprocess
import re
import sys
import os
from black_box_tests import CrawlerTest

class MultiUrlsTest(CrawlerTest):
    URI = ["https://snorrwe.github.io/crawler_test/", "kanga.pooh"]
    HERE = os.path.dirname(os.path.abspath(__file__))
    EXPECTED={
        'errors': ["\t Error while crawling site=[http://kanga.pooh] HTTPConnectionPool(host='kanga.pooh', port=80): Max retries exceeded with url: / (Caused by <class 'socket.gaierror'>: [Errno 11001] getaddrinfo failed)\r"],
        'results': [
            ('https://snorrwe.github.io/crawler_test/', '200', '404'),
            ('https://snorrwe.github.io/crawler_test/kanga2.html' , '404', '9340'),
            ('https://snorrwe.github.io/crawler_test/kanga.html' , '200', '220')
        ],
        'custom': ['[Info]Thread=[MainThread]\t -------------Yeah boiiii, done-----------------\r']
    }

    output = None

    def test_test_sanity(self):
        self.assertTrue(self.output)
        try:
            self.assertTrue(type(self.output) is unicode,
                            "Output should be of type unicode, instead got %s" % (type(self.output)))
        except NameError:  # python 3 support
            self.assertTrue(type(self.output) is str, "Output should be of type str, instead got %s" %
                            (type(self.output)))

    
    def test_found_all_pages(self):
        self.assertEqual(len(self.results['results']), len(self.EXPECTED['results']))
        for page in self.results['results']:
            self.assertTrue(page in self.EXPECTED['results'])

    def test_found_an_error(self):
        self.assertEqual(len(self.results['errors']), 1)


if __name__ == '__main__':
    unittest_main()
