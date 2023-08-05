from lollygag.utility.observer.observer import Observer

class Subject(object):
    def __init__(self):
        self.callbacks = []

    def next(self, *args):
        for callback in self.callbacks:
            if callback:
                callback(*args)

    def __call__(self, callback):
        return self.subscribe(callback)

    def subscribe(self, callback):
        assert callable(callback)
        index = None
        for i, value in enumerate(self.callbacks):
            if value is None:
                index = i
                self.callbacks[index] = callback
                break
        else:
            index = len(self.callbacks)
            self.callbacks.append(callback)
        return Observer(self, index)

    def unsubscribe(self, index):
        self.callbacks[index] = None
