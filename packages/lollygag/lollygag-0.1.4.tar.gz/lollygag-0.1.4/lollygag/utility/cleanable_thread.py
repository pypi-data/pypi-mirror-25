from threading import Thread

class CleanableThread(Thread):
    """
    A Thread object that calls on_finish when run has exited to clean up after itself
    """
    def __init__(self, on_finish, **kwargs):
        Thread.__init__(self, **kwargs)
        self.on_finish = on_finish

    def run(self):
        try:
            return Thread.run(self)
        finally:
            self.on_finish(self)
