from collections import namedtuple


class Any(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class CallableMock(object):

    ARGS_FIELDS = ['raises', 'returns', 'callback']
    Args = namedtuple('Args', ARGS_FIELDS)

    def __init__(self, **kwargs):
        self.reset(**kwargs)

    def reset(self, **kwargs):
        self.calls = []
        self.set_args(**kwargs)

    def set_args(self, **kwargs):
        assert len(kwargs.keys()) <= 1,\
            'Only one action is permitted at one time, instead got=[%s]' % len(kwargs.keys())
        for key in kwargs:
            assert key in CallableMock.ARGS_FIELDS
            raises = kwargs.get('raises', None)
            returns = kwargs.get('returns', None)
            callback = kwargs.get('callback', None)
            self.args = CallableMock.Args(raises=raises, returns=returns, callback=callback)
            break
        else:
            self.args = CallableMock.Args(callback=None, returns=None, raises=None)

    def call_count(self):
        return len(self.calls)

    def __call__(self, *a, **kw):
        try:
            result = None
            if self.args.returns:
                result = self.args.returns
            if self.args.raises:
                result = self.args.raises
                raise self.args.raises
            if self.args.callback:
                result = self.args.callback(*a, **kw)
            return result
        finally:
            self.calls.append((a, kw, result))

    def raises(self, exception):
        self.set_args(raises=exception)
        return self

    def returns(self, result):
        self.set_args(returns=result)
        return self

    def callback(self, callback):
        self.set_args(callback=callback)
        return self
