import asyncio

import aiotarantool_queue

from async_task_processor.exceptions import RetryException
from async_task_processor.primitives import TntTask


class TntTaskProcessor:
    _tasks = []
    _loop = None
    _atp = None
    _queue = None

    def __init__(self, atp, host='localhost', port=8123, user=None,
                 password=None, encoding='utf-8'):
        """Tarantool queue handler.

        Listen tarantool queue and if data there run async function.

        :param host: tarantool host
        :param port: tarantool port
        :param user: tarantool user
        :param password: tarantool password
        :param encoding: tarantool data encoding
        """
        self._atp = atp
        self._loop = atp.loop
        self._queue = aiotarantool_queue.Queue(host=host, port=port, user=user,
                                               password=password, loop=self._loop, encoding=encoding)

    def add_task(self, queue, foo, args=None, bind=None, max_workers=1, timeout=0, max_retries=0, retry_countdown=0):
        """Add task to processor

        :param queue: Tarantool queue
        :type queue: str
        :param foo: function that will work in parallel
        :param args: Function arguments
        :type args: list
        :param bind: If True, then task will be passed to function by the first argument. There is a loop and more
         specific data will be there
        :type bind: bool
        :param max_workers: Number of async copies
        :type max_workers: int
        :type timeout: int or float (seconds)
        :param max_retries: Maximum of retries, when exception is caught. You mast call self.retry.
        :type max_retries: int
        :param retry_countdown: Timeout between retries
        :type retry_countdown: int or float (seconds)
        :return:
        """
        self._tasks.extend(
            [self._make_future(queue=queue, foo=foo, args=args, bind=bind, timeout=timeout,
                               max_retries=max_retries, retry_countdown=retry_countdown) for _ in
             range(max_workers)])

    def _make_future(self, queue, foo, args, bind, timeout, max_retries, retry_countdown, retries=0):
        task = TntTask(loop=self._loop, queue_tube=self._queue.tube(queue), foo=foo, args=args, bind=bind,
                       timeout=timeout, max_retries=max_retries, retries=retries, retry_countdown=retry_countdown)
        task.set_future(asyncio.ensure_future(TntTaskProcessor._async_task_coro(task=task)))
        task.set_app(self._atp)
        return task

    @property
    def tasks(self):
        return self._tasks

    @staticmethod
    async def _async_task_coro(task):
        """

        :type task: TntTask
        :return:
        """
        while True:
            if not task.retries:
                tube = await task.queue.take(5)
                if tube:
                    task.set_tube(tube)
            if task.tube:
                arguments = [] if not task.bind else [task]
                if task.args:
                    arguments.extend(task.args)
                try:
                    await task.loop.run_in_executor(task.executor, task.foo, *arguments)
                except RetryException as exc:
                    task.app.logger.warning(exc)
                    await asyncio.sleep(task.retry_countdown)
                    continue
                task.retries = 0
                task.exception = None
                await task.tube.ack()
                task.reset()
                await asyncio.sleep(task.timeout)
