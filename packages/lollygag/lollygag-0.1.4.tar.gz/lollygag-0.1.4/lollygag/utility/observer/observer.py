class Observer(object):
    def __init__(self, subject, index):
        self.subject = subject
        self.index = index

    def unsubscribe(self):
        self.subject.unsubscribe(self.index)
