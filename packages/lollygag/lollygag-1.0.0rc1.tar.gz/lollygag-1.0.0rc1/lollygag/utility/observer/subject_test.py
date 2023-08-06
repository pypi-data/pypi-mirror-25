import unittest
from lollygag.utility.observer.subject import Subject
from lollygag.utility.test_utils import Any, CallableMock

class SubjectTests(unittest.TestCase):
    def setUp(self):
        self.subject = Subject()

class CallbackTest(SubjectTests):
    def test_calls_all_callbacks_on_next(self):
        callback1 = CallableMock()
        callback2 = CallableMock()
        self.subject(callback1)
        self.subject(callback2)
        self.assertEqual(callback1.call_count(), 0)
        self.assertEqual(callback2.call_count(), 0)
        self.subject.next()
        self.assertEqual(callback1.call_count(), 1)
        self.assertEqual(callback2.call_count(), 1)

    def test_calls_all_callbacks_every_time(self):
        callback1 = CallableMock()
        callback2 = CallableMock()
        self.subject(callback1)
        self.subject(callback2)
        self.assertEqual(callback1.call_count(), 0)
        self.assertEqual(callback2.call_count(), 0)
        for i in range(1, 25):
            self.subject.next()
            self.assertEqual(callback1.call_count(), i)
            self.assertEqual(callback2.call_count(), i)


class UnsubscribeTest(SubjectTests):
    def test_does_not_call_unsubscribed_method_again(self):
        callback1 = CallableMock()
        callback2 = CallableMock()
        self.subject(callback1)
        observable2 = self.subject(callback2)
        self.assertEqual(callback1.call_count(), 0)
        self.assertEqual(callback2.call_count(), 0)
        self.subject.next()
        self.assertEqual(callback1.call_count(), 1)
        self.assertEqual(callback2.call_count(), 1)
        observable2.unsubscribe()
        for i in range(2, 25):
            self.subject.next()
            self.assertEqual(callback1.call_count(), i)
            self.assertEqual(callback2.call_count(), 1)

class SubscribeTests(SubjectTests):
    def test_raises_AssertionError_if_called_with_None(self):
        with self.assertRaises(AssertionError):
            self.subject(None)

    def test_raises_AssertionError_if_called_with_not_callable(self):
        with self.assertRaises(AssertionError):
            self.subject(5)
        with self.assertRaises(AssertionError):
            self.subject([])
        with self.assertRaises(AssertionError):
            self.subject("asd")

    def test_can_subscribe_with_lambda(self):
        self.subject(lambda *a: a)

    def test_can_subscribe_with_function(self):
        def some_function(*args): pass
        self.subject(some_function)

    def test_can_subscribe_with_callable(self):
        class SomeCallable(object):
            def __call__(self):
                pass
        self.subject(SomeCallable())

if __name__ == '__main__':
    unittest.main()