import unittest
from lollygag.dependency_injection.inject import Inject

class InjectTests(unittest.TestCase):
    def setUp(self):
        Inject.reset()

    def test_init(self):
        result = Inject("some_feature", cache=False)
        self.assertTrue(result)

    def test_no_assertion(self):
        class Test(object):
            kanga = Inject("Kanga", cache=False)
        Inject.register_feature("Kanga", "They steal your youth!")
        result = Test().kanga
        self.assertTrue(result)
        self.assertEqual(result, "They steal your youth!")

    def test_no_feature_throws_keyerror(self):
        class Test(object):
            kanga = Inject("Kanga", cache=False)
        try:
            Test().kanga
            self.fail()
        except KeyError as error:
            self.assertEqual(str(error), str("'Feature=[Kanga] was not registered!'"))

    def test_positive_assertion_is_silent(self):
        class Test(object):
            kanga = Inject("Kanga", lambda f: isinstance(f, int), lambda f: f % 5 == 0, cache=False)
        Inject.register_feature("Kanga", 5)
        result = Test().kanga
        self.assertEqual(result, 5)

    def test_assertionerror_is_raised_if_assertion_fails(self):
        class Test(object):
            kanga = Inject("Kanga", lambda f: isinstance(f, int), cache=False)
        Inject.register_feature("Kanga", "Roo")
        try:
            Test().kanga
            self.fail()
        except AssertionError as error:
            self.assertEqual(str(error), "The value=[%s] of feature=[%s] does not match a criteria" \
                % ("Roo", "Kanga"))

    def test_factory_method(self):
        class Test(object):
            kanga = Inject("Kanga", lambda f: isinstance(f, str), cache=False)
        
        class TestKangaFactory(object):
            id = 0
            def __call__(self):
                TestKangaFactory.id += 1
                return "#%s" % TestKangaFactory.id

        Inject.register_feature("Kanga", TestKangaFactory())
        result1 = Test().kanga
        result2 = Test().kanga
        self.assertNotEqual(result1, result2)

    def test_reset(self):
        Inject.register_features(Kanga=1, Tiggers=2)
        class Test(object):
            kanga = Inject("Kanga")
            tiggers = Inject("Tiggers")

        test = Test()
        self.assertTrue(test.kanga)
        self.assertTrue(test.tiggers)
        Inject.reset()
        with self.assertRaises(KeyError):
            test.kanga
        with self.assertRaises(KeyError):
            test.tiggers

if __name__ == '__main__':
    unittest.main()
