import unittest
import asyncio
from lockchain import ChainManager


async def use_chain(link, identifier, busy_work):
    async with link:
        await busy_work
        return identifier


class BlowUpError(Exception):
    pass


async def blow_up():
    raise BlowUpError()


async def sim_chain_manager_usage(loop, n):
    mgr = ChainManager()

    tasks = []
    for i in range(n):
        # The first linked coro waits the longest....
        # The second waits second longest...
        busy_work = asyncio.sleep((n - 1) * 0.02, loop=loop)

        coro = use_chain(mgr.chain_on('test', loop), i, busy_work)
        tasks.append(loop.create_task(coro))

    results = []

    for task in asyncio.as_completed(tasks, loop=loop):
        results.append(await task)

    return results


async def sim_chain_manager_usage_with_blowup(loop):
    n = 5
    mgr = ChainManager()

    tasks = []
    for i in range(n):
        # The first linked coro waits the longest....
        # The second waits second longest..
        if i == 3:
            busy_work = blow_up()
        else:
            busy_work = asyncio.sleep((n - 1) * 0.02, loop=loop)

        coro = use_chain(mgr.chain_on('test', loop), i, busy_work)
        tasks.append(loop.create_task(coro))

    results = []

    for task in asyncio.as_completed(tasks, loop=loop):
        try:
            results.append(await task)
        except BlowUpError:
            pass

    return results


class SimpleAsyncCase(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()

    def tearDown(self):
        self.loop.close()

    def drive_coro(self, coro):
        return self.loop.run_until_complete(coro)

