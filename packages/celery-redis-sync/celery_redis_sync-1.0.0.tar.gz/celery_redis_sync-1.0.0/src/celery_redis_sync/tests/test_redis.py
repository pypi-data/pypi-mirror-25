import celery
import celery_redis_sync.redis_sync


@celery.shared_task
def test_task():
    return 42


def test_sync_backend_is_loaded_from_url_scheme(celery_test_app):
    assert isinstance(
        celery_test_app.backend,
        celery_redis_sync.redis_sync.SynchronousRedisBackend)


def test_redis_should_execute_task(celery_test_app):
    res = test_task.delay()
    # Need to call get() preventing a race condition, the test being too fast.
    res.get()
    assert res.state == 'SUCCESS'
    assert res.result == 42
