"""
Holds the Observer class
"""


class Observer(object):
    """
    Represent an Observer that's observing changes of a Subject
    """

    def __init__(self, subject, index):
        self.subject = subject
        self.__index = index
        self.__is_subscribed = True

    def unsubscribe(self):
        """
        Unsubscribes from the Subject.
        Observers should take care to call this method before being deleted
        otherwise reference to the callback that was used to subscribe might
        get sutck in memory!
        """
        self.subject.unsubscribe(self.__index)
        self.__is_subscribed = False
