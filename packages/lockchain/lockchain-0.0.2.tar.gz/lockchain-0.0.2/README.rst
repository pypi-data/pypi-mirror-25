.. image:: https://travis-ci.org/jbn/lockchain.svg?branch=master
    :target: https://travis-ci.org/jbn/lockchain
.. image:: https://ci.appveyor.com/api/projects/status/9k78nhy88v51fd69?svg=true
    :target: https://ci.appveyor.com/project/jbn/brittle-wit/branch/master
.. image:: https://coveralls.io/repos/github/jbn/lockchain/badge.svg?branch=master
    :target: https://coveralls.io/github/jbn/lockchain?branch=master 
.. image:: https://img.shields.io/pypi/dm/lockchain.svg
    :target: https://pypi.python.org/pypi/lockchain
.. image:: https://img.shields.io/pypi/v/lockchain.svg
    :target: https://pypi.python.org/pypi/lockchain
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/jbn/lockchain/master/LICENSE
.. image:: https://img.shields.io/pypi/pyversions/lockchain.svg
    :target: https://pypi.python.org/pypi/lockchain


======================
What is ``lockchain``?
======================

A ``LockChain`` allows you to create a chain of critical regions, executed 
sequentially. The underlying Lock from asyncio would actually enforce this
with a dequeue, so this library is mostly unnecessary. Had I read the code
first, I would have either not needed this or found a different solution.
Until I actually think about it though, it's still here. 

It's still useful for limiting access to some set of resources in
a namespace. If no coroutine is blocking for some resource, it's you may
get to close that resource (or reset a rate limit.)
