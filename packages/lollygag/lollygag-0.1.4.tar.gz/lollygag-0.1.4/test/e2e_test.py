from unittest import TestCase, main as unittest_main
import subprocess
import re
import os
import sys

URI = "https://snorrwe.github.io/crawler_test/"

class E2ETest(TestCase):
    output = None
    lines = None

    @classmethod
    def setUpClass(cls):
        crawler_process = subprocess.Popen(["""
import sys
sys.argv.append("-u")
sys.argv.append("%s")
sys.argv.append("-l")
sys.argv.append("info")
sys.argv.append("-t")
sys.argv.append("3")
try:
    from crawler_example import main
except ImportError:
    from test.crawler_example import main
main()
""" % (URI)
            ]
            , stdout=subprocess.PIPE, shell=True, executable=sys.executable)
        (output, error) = crawler_process.communicate()
        print(output, error)
        cls.output = output.decode("utf-8") if output else ""
        lines = cls.output.splitlines()
        cls.lines = [i for i in lines if i != '']

    def test_initialisation(self):
        self.assertTrue(self.output)
        self.assertTrue(self.lines)
        try:
            self.assertTrue(type(self.output) is unicode, "Output should be of type unicode, instead got %s" % (type(self.output)))
        except NameError: # python 3 support
            self.assertTrue(type(self.output) is str, "Output should be of type str, instead got %s" % (type(self.output)))
        expected = 13
        self.assertTrue(len(self.lines) == expected, "Output should contain %s lines, instead got %s" % (expected, len(self.lines)))

    def test_found_all_pages(self):
        found = []
        for line in self.lines:
            if(re.search(r'Link=\[.+\] StatusCode=\[\d+\] Size=\[\d+\]', line)):
                found.append(re.search(r'Link=\[.+\]', line).group(0))
        self.assertEqual(len(found), len(set(found)))
        self.assertEqual(len(found), 3)

    def test_displayed_correct_results(self):
        page_data = {}
        for line in self.lines:
            output = re.search(r'Link=\[(?P<link>.+)\] StatusCode=\[(?P<code>\d+)\] Size=\[\d+\]', line)
            if(output):
                link = output.group('link')
                code = output.group('code')
                page_data[link] = code
        self.assertTrue('%s' % (URI)in page_data)
        self.assertTrue('%skanga.html' % (URI) in page_data)
        self.assertTrue('%skanga2.html' % (URI) in page_data)
        self.assertEqual(page_data['%s' % (URI)], '200')
        self.assertEqual(page_data['%skanga.html' % (URI)], '200')
        self.assertEqual(page_data['%skanga2.html' % (URI)], '404')

if __name__ == '__main__':
    unittest_main()
