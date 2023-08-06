import asyncio


__title__ = "lockchain"
__description__ = "Async-based context manager that enforces FIFO processing"
__uri__ = "https://github.com/jbn/brittle_wit"
__doc__ = __description__ + " <" + __uri__ + ">"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2017 John Bjorn Nelson"
__version__ = "0.0.2"
__author__ = "John Bjorn Nelson"
__email__ = "jbn@abreka.com"


class _Link:

    __slots__ = '_lock_chain', '_antecedent', '_consequent'

    def __init__(self, lock_chain, antecedent_lock, consequent_lock):
        """
        :param lock_chain: the LockChain this Link belongs to
        :param antecedent_lock: the lock that must be acquired before the
            context body can execute
        :param consequent_lock: the lock that must be held until execution
            completes
        """
        self._lock_chain = lock_chain
        self._antecedent = antecedent_lock
        self._consequent = consequent_lock

    @property
    def consequent(self):
        return self._consequent

    async def _acquire(self):
        # Immediately acquire the consequent lock. The next link uses this as
        # its antecedent. So, the next link cannot progress until this link
        # releases its consequent.
        await self._consequent.acquire()

        # Attempt to acquire the antecedent. This acts as a barrier to
        # execution. Continue once the antecedent completes.
        async with self._antecedent:
            pass  # This is a barrier

    def _release(self):
        # Release the consequent so that the next coro in the chain can go.
        self._consequent.release()

        # Allow the LockChain to do maintenance.
        self._lock_chain._notify_finished(self)

    async def __aenter__(self):
        await self._acquire()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._release()


def _on_empty_noop(name):
    return


class LockChain:
    """
    A locking, synchronization context manager that enforces FIFO ordering.
    """

    def __init__(self, name=None, on_empty_callback=None):
        """
        :param name: the name of this LockChain
        :param on_empty_callback: function-like object called every time
            there are no items waiting in the lock chain. Takes one
            arguments, the name of this LockChain.
        """
        self._name = name
        self._consequent = None
        self._empty_callback = on_empty_callback or _on_empty_noop

    @property
    def name(self):
        return self._name

    def __bool__(self):
        return self._consequent is not None

    def _notify_finished(self, link):
        if self._consequent is link.consequent:
            self._consequent = None
            self._empty_callback(self.name)

    def link(self, loop=None):
        """
        Create a new link and return it for use in a `with` statment.

        :param loop: loop kto create lock in (defaults to current loop)
        """
        antecedent = self._consequent or asyncio.Lock(loop=loop)
        self._consequent = asyncio.Lock(loop=loop)

        return _Link(self, antecedent, self._consequent)


class ChainManager:
    """
    A name space for LockChains that deletes unneeded chains.
    """

    __slots__ = '_chains'

    def __init__(self):
        self._chains = {}  # k -> LinkChain

    def is_chain_empty(self, k):
        """
        :return: True if the chain at key k is empty
        """
        return k not in self._chains

    def all_chains_empty(self):
        """
        :return: True if the all the chains are empty
        """
        return not self._chains

    def _notify_finished(self, k):
        """
        Notify this ChainManager when a particular chain is empty.
        """
        del self._chains[k]

    def chain_on(self, k, loop=None):
        """
        Add a link to the chain at key, k.

        WARNING: Use this as ``async with mgr.chain_on(k)``.
                 Don't take a link; do other stuff; then use it. If your
                 other stuff fails outside of the context, the chained
                 coros will wait forever!

        :param k: the requested LockChain
        :param loop: the event loop

        :return: a link context
        """
        chain = self._chains.get(k)

        if chain is None:
            chain = LockChain(k, self._notify_finished)
            self._chains[k] = chain

        return chain.link(loop)
