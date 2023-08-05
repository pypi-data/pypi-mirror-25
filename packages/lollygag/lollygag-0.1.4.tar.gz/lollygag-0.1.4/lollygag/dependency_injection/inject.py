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

    assertions are used to further specify a feature's required interface

    Example:
        class MyClass(object):
            some_feature = Inject("feature", assertion1, assertion2)
            some_factory = Inject("another_feature", return_factory=True)

    """
    features = {}

    @staticmethod
    def register_feature(name, feature):
        Inject.features[name] = feature

    @staticmethod
    def register_features(**dictionary):
        for key in dictionary:
            Inject.features[key] = dictionary[key]

    @staticmethod
    def reset():
        Inject.features = {}
        CACHE.clear()

    def __init__(self, key, *assertions, **config):
        self.key = key
        self.assertions = assertions
        self.init_config(config)

    def init_config(self, config):
        self.config = config
        for key in DEFAULT_CONFIG:
            if key not in self.config:
                self.config[key] = DEFAULT_CONFIG[key]

    def __get__(self, instance, owner):
        if self.config["cache"] and self.key in CACHE and CACHE[self.key]:
            return CACHE[self.key]
        return self.request()

    def request(self):
        try:
            feature = Inject.features[self.key]
            if callable(feature) and not self.config["return_factory"]:
                feature = feature()
            if self.config["cache"]:
                CACHE[self.key] = feature
            for assertion in self.assertions:
                self._make_assertion(assertion, feature)
            return feature
        except KeyError:
            raise KeyError("Feature=[%s] was not registered!" % self.key)

    def _make_assertion(self, assertion, obj):
        assert assertion(obj), "The value=[%s] of feature=[%s] does not match a criteria" \
                                 % (obj, self.key)
