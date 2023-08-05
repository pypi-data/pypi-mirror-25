import sys
import traceback
from concurrent.futures import ThreadPoolExecutor

from async_task_processor.exceptions import MaxRetriesExceed, RetryException


class BaseTask(object):
    loop = None
    type = None
    coroutine_future = None
    app = None
    foo = None
    executor = None
    args = None
    bind = None
    timeout = None
    max_retries = None
    retries = 0

    def __init__(self, loop, task_type, foo, args, bind, timeout, max_retries, retry_countdown, retries=0):
        """

        :type loop: asyncio.AbstractEventLoop
        :param task_type:
        :param foo:
        :param args:
        :param bind:
        :param timeout:
        :param max_retries:
        :param retries:
        """
        self.loop = loop
        self.type = task_type
        self.foo = foo
        self.args = args
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.bind = bind
        self.timeout = timeout or 0.01
        self.max_retries = max_retries
        self.retry_countdown = retry_countdown or 0.01
        self.retries = retries
        self.exception = None

    def retry(self, max_retries=None, retry_countdown=None):
        """Retry task execution

        :param max_retries:
        :param retry_countdown:
        :return:
        """
        if max_retries:
            self.max_retries = max_retries
        if retry_countdown:
            self.retry_countdown = retry_countdown
        if self.retries == self.max_retries:
            try:
                raise MaxRetriesExceed(
                    'Max retries exceeded for exception {exception}. Traceback:\n {traceback}'.format(
                        exception=sys.exc_info()[0],
                        traceback=traceback.format_exc()))
            except MaxRetriesExceed as exc:
                self.app.logger.error(exc)
            self.app.tasks.remove(self)
            if not self.app.tasks:
                exit(1)
            self.coroutine_future.cancel()

        self.retries += 1
        raise RetryException(
            'Trying to retry task on exception: {exception}. Retry #{retry}. Traceback:\n {traceback}'.format(
                exception=repr(sys.exc_info()[0]), retry=self.retries, traceback=traceback.format_exc()))

    def set_future(self, future):
        """

        :type future: asyncio.Future
        :return:
        """
        self.coroutine_future = future

    def set_app(self, atp):
        """

        :type atp: async_task_processor.atp.ATP
        :return:
        """
        self.app = atp
        self.app.add_tasks(*[self])
