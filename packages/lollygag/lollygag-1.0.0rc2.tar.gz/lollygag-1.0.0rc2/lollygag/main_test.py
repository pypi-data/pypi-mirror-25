import unittest
from lollygag.main import separate_urls_by_domain, subscribe_to_crawler, register
from lollygag.utility.test_utils import Any, CallableMock


class Test_separate_urls_by_domain(unittest.TestCase):

    def test_separates_correctly(self):
        result = separate_urls_by_domain(
            ["github.com", "youtube.com", "youtube.com/1", "asd.youtube.com"])
        expected = {
            'github.com': ["github.com"],
            'youtube.com': ["youtube.com", "youtube.com/1"],
            'asd.youtube.com': ["asd.youtube.com"]
        }
        self.assertEqual(result, expected)

    def test_does_not_accept(self):
        with self.assertRaises(AssertionError):
            separate_urls_by_domain("asd")
        with self.assertRaises(AssertionError):
            separate_urls_by_domain(1)
        with self.assertRaises(AssertionError):
            separate_urls_by_domain({})
        with self.assertRaises(AssertionError):
            separate_urls_by_domain((1,))


class Test_register_events(unittest.TestCase):

    def setUp(self):
        self.crawler = Any(on_start=CallableMock(),
                           on_finish=CallableMock(),
                           on_interrupt=CallableMock())

    def test_subscribes_to_on_finish_with_single_callback(self):
        subs = {
            'on_finish': lambda *a, **kw: None
        }
        subscribe_to_crawler(self.crawler, **subs)
        self.assertEqual(self.crawler.on_finish.call_count(), 1)

    def test_subscribes_to_on_start_with_single_callback(self):
        subs = {
            'on_start': lambda *a, **kw: None
        }
        subscribe_to_crawler(self.crawler, **subs)
        self.assertEqual(self.crawler.on_start.call_count(), 1)

    def test_subscribes_to_on_interrupt_with_single_callback(self):
        subs = {
            'on_interrupt': lambda *a, **kw: None
        }
        subscribe_to_crawler(self.crawler, **subs)
        self.assertEqual(self.crawler.on_interrupt.call_count(), 1)

    def test_subscribes_to_on_start_with_list(self):
        subs = {
            'on_start': [lambda *a, **kw: None] * 4
        }
        subscribe_to_crawler(self.crawler, **subs)
        self.assertEqual(self.crawler.on_start.call_count(), 4)


class Test_register(unittest.TestCase):

    def setUp(self):
        self.crawler = Any(on_start=CallableMock(),
                           on_finish=CallableMock(),
                           on_interrupt=CallableMock())

    def test_subscribes_to_on_start(self):
        register(self.crawler, 'on_start', lambda *a, **kw: None)
        self.assertEqual(self.crawler.on_start.call_count(), 1)

    def test_subscribes_to_on_finish(self):
        register(self.crawler, 'on_finish', lambda *a, **kw: None)
        self.assertEqual(self.crawler.on_finish.call_count(), 1)

    def test_subscribes_to_on_interrupt(self):
        register(self.crawler, 'on_interrupt', lambda *a, **kw: None)
        self.assertEqual(self.crawler.on_interrupt.call_count(), 1)

    def test_raises_keyerror_on_unknown_type(self):
        with self.assertRaises(KeyError):
            register(self.crawler, 'unknown_type', lambda *a, **kw: None)

    def test_raises_assertion_error_on_empty_crawler(self):
        with self.assertRaises(AssertionError):
            register(None, 'on_start', lambda *a, **kw: None)

    def test_raises_assertion_error_on_not_callable_callback(self):
        with self.assertRaises(AssertionError):
            register(self.crawler, 'on_start', "")
        with self.assertRaises(AssertionError):
            register(self.crawler, 'on_start', 1)
        with self.assertRaises(AssertionError):
            register(self.crawler, 'on_start', {})
        with self.assertRaises(AssertionError):
            register(self.crawler, 'on_start', [])


if __name__ == '__main__':
    unittest.main()
