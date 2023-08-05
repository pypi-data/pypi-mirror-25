====================
Async task processor
====================

Used to distribute tasks between configurable workers.

Features
--------

- simple definition of a task as a normal function.
- simple task processor is used for periodic tasks.
- tarantool processor is  used for listen tarantool queue and trigger task when data comes.
- ability to retry on error (max_retries and retry_countdown options).
- ability to bind task as self option to worker function.

TODO's
------
- [ ] Tests
- [ ] Console utils

Installation
------------

As usually use pip:

.. code-block:: bash

    pip install async-task-processor

Usage examples
--------------

**Periodic task processor example:**

.. code-block:: python

    import time

    from async_task_processor import ATP, TaskProcessor
    from examples import logger


    # first test function
    def test_func_one(sleep_time, word):
        """

        :type sleep_time: int
        :type word: str
        :return:
        """
        logger.info('start working')
        time.sleep(sleep_time)
        logger.info('Job is done. Word is: %s' % word)


    # second test function
    def test_func_second(sleep_time, word):
        """

        :type sleep_time: int
        :type word: str
        :return:
        """
        logger.info('start working')
        time.sleep(sleep_time)
        logger.info('Job is done. Word is: %s' % word)


    # third function with exception
    def test_func_bad(self, sleep_time, word):
        """

        :type self: async_task_processor.Task
        :type sleep_time: int
        :type word: str
        :return:
        """
        logger.info('start working')
        try:
            a = 1 / 0
        except ZeroDivisionError:
            # optionally you can overload max_retries and retry_countdown here
            self.retry()
        time.sleep(sleep_time)
        logger.info('Job is done. Word is: %s' % word)


    atp = ATP(asyncio_debug=True)
    task_processor = TaskProcessor(atp=atp)

    # Add function to task processor
    task_processor.add_task(test_func_one, args=[5, 'first hello world'], max_workers=5, timeout=1,
                            max_retries=5, retry_countdown=1)

    # Add one more function to task processor
    task_processor.add_task(test_func_second, args=[3, 'second hello world'], max_workers=5, timeout=1,
                            max_retries=5, retry_countdown=1)

    # Add one more bad function with exception. This function will raise exception and will retry it,
    # then when retries exceeded, workers of this func will stop one by one with exception MaxRetriesExceeded
    # bind option make Task as self argument
    task_processor.add_task(test_func_bad, args=[3, 'second hello world'], bind=True, max_workers=2, timeout=1,
                            max_retries=3, retry_countdown=3)
    # Start async-task-processor
    atp.start()

**Tarantool task processor example:**

.. code-block:: python

    import asyncio
    import time

    import aiotarantool_queue

    from async_task_processor import ATP, TntTaskProcessor
    from examples import logger

    TARANTOOL_QUEUE = 'test_queue'
    TARANTOOL_HOST = 'localhost'
    TARANTOOL_PORT = 3301
    TARANTOOL_USER = None
    TARANTOOL_PASS = None


    def put_messages_to_tarantool(messages_count=1, queue_name='test_queue', host='localhost', port=3301, user=None,
                                  password=None):
        """Put some test messages to tarantool queue

        :param messages_count: messages number to put in queue
        :param queue_name: tarantool queue name
        :type queue_name: str
        :param host: tarantool host
        :param port: tarantool port
        :param user: tarantool user
        :param password: tarantool password
        :return:
        """

        async def put_job(queue, i):
            tube = queue.tube(queue_name)
            await tube.put(dict(num=i, first_name='Jon', last_name='Smith'))

        loop = asyncio.get_event_loop()
        queue = aiotarantool_queue.Queue(host=host, port=port, user=user, password=password)
        put_tasks = [asyncio.async(put_job(queue, i)) for i in range(messages_count)]
        loop.run_until_complete(asyncio.wait(put_tasks))
        loop.run_until_complete(queue.close())
        loop.close()


    # Let's put messages to tarantool
    put_messages_to_tarantool(100, TARANTOOL_QUEUE, host=TARANTOOL_HOST, port=TARANTOOL_PORT,
                              user=TARANTOOL_USER, password=TARANTOOL_PASS)


    # Test function
    def test_func(self, sleep_time, word):
        """

        :type self: async_task_processor.TntTask
        :type sleep_time: int
        :type word: str
        :return:
        """
        logger.info('start working')
        time.sleep(sleep_time)
        logger.info('Job is done. Word is %s. Data is %s. ' % (word, self.data))


    atp = ATP(asyncio_debug=True)
    task_processor = TntTaskProcessor(atp=atp, host=TARANTOOL_HOST, port=TARANTOOL_PORT, user=TARANTOOL_USER,
                                      password=TARANTOOL_PASS)

    # Add function to task processor. Tarantool data from queue will be in `self` argument in function. 20 parallel workers
    # will be started.
    task_processor.add_task(foo=test_func, queue=TARANTOOL_QUEUE, args=[1, 'hello world'], bind=True, max_workers=20,
                            max_retries=5, retry_countdown=1)
    # Start async-task-processor
    atp.start()
