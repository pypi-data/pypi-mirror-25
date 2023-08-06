=================
celery_redis_sync
=================

Synchronous Redis result store backend.

This fixes the issue that the redis publish/subscribe channels are currently
not removed properly by the default (asynchronous) redis backend, see
https://github.com/celery/celery/issues/3812. (Our "solution" is to never
create any channels in the first place.)


Usage
=====

Make sure the ``celery_redis_sync`` module is importable, and then simply
specify a ``redis+sync://`` URL in your celery configuration ``result_backend``
setting instead of the built-in ``redis://`` URL scheme.


Run tests
=========

Using `tox`_ and `py.test`_. Maybe install ``tox`` (e.g. via ``pip install tox``)
and then simply run ``tox``.

For the integration tests you need to have the redis binary installed (tests
start `their own server`_).

.. _`tox`: http://tox.readthedocs.io/
.. _`py.test`: http://pytest.org/
.. _`their own server`: https://pypi.python.org/pypi/testing.redis
