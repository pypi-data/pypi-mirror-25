"""
Holds the Inject class.
"""
import json


DEFAULT_CONFIG = {
    "return_factory": False,
    "cache": True
}

CACHE = {}


class Inject(object):
    """
    Represents a required field in a class
    On __get__ injects the required feature from features is present
    raises an error is it's not present

    specifications are used to further specify a feature's required interface

    Example:
        class MyClass(object):
            some_feature = Inject("feature", assertion1, assertion2)
            some_factory = Inject("another_feature", return_factory=True)

    """
    features = {}

    @staticmethod
    def register_feature(name, feature):
        """
        Registers a new injectable feature by name.
        """
        Inject.features[name] = feature

    @staticmethod
    def register_features(**dictionary):
        """
        Registers injectable features.

        Example:
            my_winnie = Inject('winnie').request() # not ok
            Inject.register_features(foo='bar', winnie=Pooh())
            my_winnie = Inject('winnie').request() # ok
        """
        for key in dictionary:
            Inject.register_feature(key, dictionary[key])

    @staticmethod
    def reset():
        """
        Removes all features from Inject and resets the cache.
        """
        Inject.features = {}
        CACHE.clear()

    def __init__(self, key, *assertions, **config):
        self.key = key
        self.specifications = assertions
        self.init_config(config)

    def init_config(self, config):
        """
        Initializes the configuration of the instance.
        """
        self.config = config
        for key in DEFAULT_CONFIG:
            if key not in self.config:
                self.config[key] = DEFAULT_CONFIG[key]
        self.config_key = json.JSONEncoder().encode(self.config)

    def __get__(self, instance, owner):
        return self.request()

    def request(self):
        """
        Return the feature by the instance's key.
        Raises KeyError if the feature isn't registered at the time of request.
        Raises AssertionError if the registered feature fails to
        fulfill a specification of the instance.
        """
        try:
            if self.config["cache"] and self.key in CACHE and self.config_key in CACHE[self.key]:
                return CACHE[self.key][self.config_key]
            feature = Inject.features[self.key]
            if callable(feature) and not self.config["return_factory"]:
                feature = feature()
            if self.config["cache"]:
                if self.key not in CACHE:
                    CACHE[self.key] = {}
                CACHE[self.key][self.config_key] = feature
            for assertion in self.specifications:
                self._make_assertion(assertion, feature)
            return feature
        except KeyError:
            raise KeyError("Feature=[%s] was not registered!" % self.key)

    def _make_assertion(self, assertion, obj):
        assert assertion(obj), "The value=[%s] of feature=[%s] does not match a criteria" \
            % (obj, self.key)
