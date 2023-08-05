from lollygag.dependency_injection.inject import Inject
from lollygag.dependency_injection.requirements import HasMethods, HasAttributes

class WorkService(object):
    threading = Inject("threading", \
                    HasMethods("Thread", "Lock"))
    config_service = Inject("config_service", HasAttributes("threads"))
    log_service = Inject("log_service", HasMethods("debug", "info"))
    queue = Inject("queue", HasMethods("put", "get", "task_done", "join"))
    __count = 0

    def __init__(self):
        self.request_lock = self.threading.Lock()
        worker_count = int(self.config_service.threads)
        if worker_count < 1:
            raise ValueError("Thread count cannot be less than 1!")
        self.__init_workers(worker_count)

    def __init_workers(self, number):
        for i in range(number):
            worker = self.threading.Thread(target=self.__worker, name="WSc--%s" % i)
            worker.daemon = True
            worker.start()

    def request_work(self, target, blocking=True):
        assert target is not None
        assert callable(target)
        return self.queue.put(target, blocking)

    def terminate_all(self, graceful=False):
        self.log_service.debug("-----------------Terminate request received-----------------")
        if graceful:
            self.queue.join()

    def active_count(self):
        return self.__count

    def __worker(self):
        while 1:
            task = self.queue.get()
            self.__count += 1
            task()
            self.__count -= 1
            self.queue.task_done()
