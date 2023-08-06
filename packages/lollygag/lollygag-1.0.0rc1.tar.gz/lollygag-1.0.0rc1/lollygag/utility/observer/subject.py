"""
Holds the Subject class.
"""
from lollygag.utility.observer.observer import Observer


class Subject(object):
    """
    Represent a subject of interest for Observers.
    """

    def __init__(self):
        self.callbacks = []

    def next(self, *args, **kwargs):
        """
        Calls subscribers with passed args.
        """
        for callback in self.callbacks:
            if callback:
                callback(*args, **kwargs)

    def __call__(self, callback):
        return self.subscribe(callback)

    def subscribe(self, callback):
        """
        Subscribes to the Subject to be notified of changes.
        """
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
        """
        Unsubscribes index from the Subject.
        Internal method, users should use the Observer.unsubscribe method
        on the Observer returned by subscribe.
        """
        self.callbacks[index] = None
