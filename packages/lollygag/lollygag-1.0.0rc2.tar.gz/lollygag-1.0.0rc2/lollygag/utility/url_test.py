import unittest
from lollygag.utility.url import get_domain

class get_domainTest(unittest.TestCase):
    def test_should_recognise_http(self):
        result = get_domain("http://winnie.thepooh")
        self.assertEqual(result, "winnie.thepooh")

    def test_should_recognise_https(self):
        result = get_domain("https://winnie.thepooh")
        self.assertEqual(result, "winnie.thepooh")

    def test_should_remove_www(self):
        result = get_domain("http://www.winnie.thepooh")
        self.assertEqual(result, "winnie.thepooh")

    def test_should_remove_last_per(self):
        result = get_domain("http://www.winnie.thepooh/")
        self.assertEqual(result, "winnie.thepooh")

    def test_should_recognise_ip(self):
        result = get_domain("http://123.125.255.1")
        self.assertEqual(result, "123.125.255.1")

    def test_raises_on_None(self):
        with self.assertRaises(AssertionError):
            get_domain(None)
