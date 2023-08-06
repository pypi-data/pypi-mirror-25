import unittest
import threading
from tl.testing.thread import ThreadJoiner, ThreadAwareTestCase
from lollygag.services.work.work_service import WorkService, get_labels
from lollygag.dependency_injection.inject import Inject
from lollygag.utility.test_utils import Any, CallableMock
try:
    import Queue
except ImportError:
    import queue as Queue

threading_mock = Any(Thread=CallableMock())
config_mock = Any(threads=1)
queue_mock = Any(put=CallableMock(), get=CallableMock(), task_done=CallableMock(), join=CallableMock())
log_service_mock = Any(debug=CallableMock(), info=CallableMock())


class WorkServiceTests(unittest.TestCase):
    def setUp(self):
        Inject.reset()
        self.startMock = CallableMock()
        threading_mock.Thread.reset(returns=Any(daemon=False, start=self.startMock))
        Inject.register_feature("threading", threading_mock)
        Inject.register_feature("config_service", config_mock)
        Inject.register_feature("queue", lambda: queue_mock)
        Inject.register_feature("log_service", log_service_mock)

    def tearDown(self):
        Inject.reset()


class WorkServiceInitTests(WorkServiceTests):
    def test_init(self):
        service = WorkService()
        self.assertTrue(service)
        self.assertEqual(1, service.threading.Thread.call_count())
        self.assertEqual(1, self.startMock.call_count())

    def test_init_multiple_workers(self):
        config_mock.threads = 5
        service = WorkService()
        self.assertTrue(service)
        self.assertEqual(5, service.threading.Thread.call_count())
        self.assertEqual(5, self.startMock.call_count())
        config_mock.threads = 1


class WorkerService_request_work_Tests(WorkServiceTests, ThreadAwareTestCase):
    def setUp(self):
        super(WorkerService_request_work_Tests, self).setUp()
        Inject.register_feature("queue", Queue.Queue)
        Inject.register_feature("threading", threading)

    def test_worker_thread_calls_argument(self):
        try:
            with ThreadJoiner(0.5):
                service = WorkService()
                requested_work = CallableMock()
                service.request_work(requested_work)
        except RuntimeError:
            pass
        self.assertEqual(requested_work.call_count(), 1)

    def test_None_as_argument_raises(self):
        with self.assertRaises(AssertionError):
            service = WorkService()
            service.request_work(None)

    def test_invalid_argument_raises(self):
        with self.assertRaises(AssertionError):
            service = WorkService()
            service.request_work(123)
        with self.assertRaises(AssertionError):
            service = WorkService()
            service.request_work("kanga")


class WorkService_terminate_all_Tests(WorkServiceTests):
    def test_does_not_join_the_queue_by_default(self):
        service = WorkService()
        service.terminate_all()
        self.assertEqual(queue_mock.join.call_count(), 0)

    def test_joins_the_queue_if_graceful(self):
        service = WorkService()
        service.terminate_all(True)
        self.assertEqual(queue_mock.join.call_count(), 1)


class get_labels_Tests(unittest.TestCase):
    def test_returns_desired_numbers(self):
        expected = [0, 1, 2, 3, 4]
        actual = []
        for i in get_labels(5, actual):
            actual.append(i)
        self.assertEqual(expected, actual)

    def test_returns_gaps_in_sequences(self):
        expected = [0, 1, 2, 3, 4, 5]
        actual = [0, 2, 4]
        for i in get_labels(3, actual):
            actual.append(i)
        self.assertEqual(set(expected), set(actual))

    def test_finds_gaps_in_unordered(self):
        expected = [0, 1, 2, 3, 4, 5]
        actual = [4, 4, 0, 2]
        for i in get_labels(3, actual):
            actual.append(i)
        self.assertEqual(set(expected), set(actual))


if __name__ == '__main__':
    unittest.main()
