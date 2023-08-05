class Any(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

class CallableMock(object):
    def __init__(self, **kwargs):
        self.reset(**kwargs)

    def reset(self, **kwargs):
        self.calls = []
        self.args = kwargs

    def call_count(self):
        return len(self.calls)

    def __call__(self, *a, **kw):
        try:
            result = None
            if "returns" in self.args:
                result = self.args["returns"]
            if "raises" in self.args:
                result = self.args["raises"]
                raise self.args["raises"]
            if "callback" in self.args:
                result = self.args["callback"](*a, **kw)
            return result
        finally:
            self.calls.append((a, kw, result))
