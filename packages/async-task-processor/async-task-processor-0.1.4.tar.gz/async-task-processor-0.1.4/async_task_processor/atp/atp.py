import asyncio
import logging
import signal
import sys

from async_task_processor.exceptions import ATPException


class ATP(object):
    tasks = []
    logger = None
    sentry = {'client': None, 'level': None}
    loop = None

    def __init__(self, loop=None, asyncio_debug=False):
        """

        :type loop: uvloop.Loop
        :type asyncio_debug: bool
        """
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.loop = loop or asyncio.get_event_loop()
        self.loop.set_debug(asyncio_debug)
        self.logger = logging.getLogger("async_task_processor")

    def _signal_handler(self):
        """Signal handler

        :return:
        """
        self.logger.info("canceling all pending tasks ...")
        for task in asyncio.Task.all_tasks():
            task.cancel()
        self.logger.info("all tasks canceled, exit...")
        sys.exit(0)

    def add_tasks(self, *tasks):
        """Add tasks

        :param tasks:
        :return:
        """
        self.tasks.extend(tasks)

    def start(self):
        """Start async task workers

        :return:
        """
        if not self.tasks:
            raise ATPException(
                'you must add some task`s in TaskRunner instance first, use add_tasks method')
        for sig in ('SIGINT', 'SIGTERM'):
            self.loop.add_signal_handler(getattr(signal, sig), self._signal_handler)
        try:
            self.loop.run_until_complete(asyncio.gather(*[task.coroutine_future for task in self.tasks]))
        except asyncio.CancelledError:
            pass
        self.loop.run_forever()
