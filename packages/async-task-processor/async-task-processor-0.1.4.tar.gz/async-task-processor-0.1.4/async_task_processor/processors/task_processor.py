import asyncio

from async_task_processor.exceptions import RetryException
from async_task_processor.primitives import Task


class TaskProcessor:
    _tasks = []
    _loop = None
    _atp = None

    def __init__(self, atp):
        """

        :type atp: async_task_processor.atp.ATP
        """
        self._loop = atp.loop
        self._atp = atp

    @property
    def tasks(self):
        return self._tasks

    def add_task(self, foo, args=None, bind=None, max_workers=1, timeout=0, max_retries=0, retry_countdown=0):
        """Add task to processor

        :param foo: function that will work in parallel
        :param args: function arguments
        :type args: list
        :param bind: If True, then task will be passed to function by the first argument. There is a loop and more
         specific data will be there
        :type bind: bool
        :param max_workers: Number of async copies
        :type max_workers: int
        :type timeout: int or float (seconds)
        :param max_retries: Maximum of retries, when the exception is caught. You mast call self.retry.
        :type max_retries: int
        :param retry_countdown: Timeout between retries
        :type retry_countdown: int or float (seconds)
        :return:
        """
        self._tasks.extend(
            [self._make_future(foo=foo, args=args, bind=bind, timeout=timeout, max_retries=max_retries,
                               retry_countdown=retry_countdown) for _ in range(max_workers)])

    def _make_future(self, foo, args, bind, timeout, max_retries, retry_countdown, retries=0):
        task = Task(loop=self._loop, foo=foo, args=args, bind=bind, timeout=timeout,
                    max_retries=max_retries, retries=retries, retry_countdown=retry_countdown)
        task.set_future(asyncio.ensure_future(TaskProcessor._async_task_coro(task=task)))
        task.set_app(self._atp)
        return task

    @staticmethod
    async def _async_task_coro(task):
        """

        :type task: async_task_processor.primitives.task.Task
        :return:
        """
        while True:
            arguments = [] if not task.bind else [task]
            if task.args:
                arguments.extend(task.args)
            try:
                await asyncio.ensure_future(task.loop.run_in_executor(task.executor, task.foo, *arguments))
            except RetryException as exc:
                await asyncio.sleep(task.retry_countdown)
                task.app.logger.warning(exc)
                continue
            task.retries = 0
            task.exception = None
            await asyncio.sleep(task.timeout)
