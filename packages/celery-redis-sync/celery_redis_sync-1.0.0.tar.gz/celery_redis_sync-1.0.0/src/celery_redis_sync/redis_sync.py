import celery.backends.base
import celery.backends.redis


def select_backend(**kw):
    """Override the built-in redis:// backend URL to also support redis+sync://
    """
    url = kw.get('url', '')
    # See celery.app.backends.by_url
    if url.startswith('sync'):
        cls = SynchronousRedisBackend
    else:
        cls = celery.backends.redis.RedisBackend
    return cls(**kw)


class SynchronousRedisBackend(
        celery.backends.base.SyncBackendMixin,
        celery.backends.redis.RedisBackend):
    """Synchronous Redis result backend.

    This fixes the celery issue that these channels are not removed properly,
    which is the main reason for this backend's existence (our "solution" is to
    never create any channels in the first place), see
    <https://github.com/celery/celery/issues/3812>.

    This implementation works by inheriting from the default (asynchronous)
    RedisBackend, and surgically removing anything to do with async and pubsub:

    * Inherit _first_ from SyncBackendMixin, so any API methods will be found
      there instead of AsyncBackendMixin (from which RedisBackend inherits).
    * Change the ResultConsumer factory to just return None. It's called in
      __init__() to populate self.result_consumer, which is only used in
      on_task_call(), which we also change to a noop.
    * Don't create a ``publish`` channel in set(), since we won't have a
      ResultConsumer that would ``subscribe`` to it.
    """

    def ResultConsumer(self, *args, **kw):
        return None

    def on_task_call(self, *args, **kw):
        pass

    def _set(self, key, value):
        # We omit the self.client.publish() call.
        if self.expires:
            self.client.setex(key, self.expires, value)
        else:
            self.client.set(key, value)
