from async_task_processor.primitives.base_task import BaseTask


class TntTask(BaseTask):
    queue = None
    data = None
    _tube = None

    def __init__(self, loop, queue_tube, foo, args, bind, timeout, max_retries, retry_countdown, retries):
        self.queue = queue_tube
        super().__init__(loop, type(self), foo, args, bind, timeout, max_retries, retry_countdown, retries)

    def set_tube(self, tube):
        self._tube = tube
        self._set_data()

    def _set_data(self):
        self.data = self.tube.data

    def reset(self):
        self._tube, self.data = None, None

    @property
    def tube(self):
        return self._tube
