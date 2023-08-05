class HasAttributes(object):
    """
    Functor style object for checking if an object obj has the specified attributes
    Example:
        check_has_bar = HasAttributes("foo")
        ...
        if check_has_bar(obj):
            # obj has an attribute named foo
            # do something with obj.foo
    """
    def __init__(self, *keys):
        self._keys = keys

    def __call__(self, obj):
        return self.evaluate(obj)

    def evaluate(self, obj):
        for key in self._keys:
            assert hasattr(obj, key), "Attribute named=[%s] is not found in obj=[%s]" % (key, obj)
        return True

    def get_keys(self):
        return self._keys

class HasMethods(HasAttributes):
    """
    Functor style object for checking if an object obj has the specified attributes
    and those attributes are callable
    Example:
        check_has_bar = HasAttributes("bar")
        ...
        if check_has_bar(obj):
            # obj has a method named bar
            # do something with obj.bar()
    """
    def evaluate(self, obj):
        for key in self._keys:
            method = getattr(obj, key)
            assert callable(method), "Attribute named=[%s] is not callable in obj=[%s]" % (key, obj)
        return True
