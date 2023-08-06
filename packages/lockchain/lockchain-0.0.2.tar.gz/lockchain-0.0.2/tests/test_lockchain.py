import unittest
from tests import *
from unittest.mock import Mock
import asyncio
import random
from lockchain import LockChain, ChainManager


class TestLockChain(SimpleAsyncCase):

    def test_manual_chaining(self):
        async def test_link_usage(chain, name, log):
            async with chain.link():
                await asyncio.sleep(random.random() * 0.01)
                self.assertTrue(chain)  # Not empty
                log.append(name)

        lock_chain = LockChain()
        self.assertFalse(lock_chain)

        names, results, tasks = list(range(100)), [], []

        for name in names:
            coro = test_link_usage(lock_chain, name, results)
            tasks.append(self.loop.create_task(coro))

        self.loop.run_until_complete(asyncio.gather(*tasks))
        self.assertEqual(names, results)
        self.assertFalse(lock_chain)


class TestChainManager(SimpleAsyncCase):

    def test_basic(self):
        n = 5
        result = self.drive_coro(sim_chain_manager_usage(self.loop, n))
        self.assertEqual(result, list(range(n)))

    def test_chain_manager_with_failing_coro(self):
        coro = sim_chain_manager_usage_with_blowup(self.loop)
        result = self.drive_coro(coro)

        # Number 3 blows up
        self.assertEqual(result, [0, 1, 2, 4])

    def test_is_line_empty(self):
        mgr = ChainManager()
        self.assertTrue(mgr.is_chain_empty('main_line'))
        self.assertTrue(mgr.is_chain_empty('second_line'))
        mgr.chain_on('main_line')
        self.assertFalse(mgr.is_chain_empty('main_line'))
        self.assertTrue(mgr.is_chain_empty('second_line'))

    def test_all_lines_empty(self):
        mgr = ChainManager()
        self.assertTrue(mgr.all_chains_empty())
        mgr.chain_on('main_line')
        self.assertFalse(mgr.all_chains_empty())
