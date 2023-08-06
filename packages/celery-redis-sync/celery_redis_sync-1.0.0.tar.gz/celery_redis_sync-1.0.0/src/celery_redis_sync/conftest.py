import celery.contrib.testing.app
import pytest
import testing.redis


@pytest.fixture(scope='session')
def redis_server():
    server = testing.redis.RedisServer()
    yield server
    server.stop()


@pytest.fixture('session')
def celery_test_app(redis_server):
    app = celery.contrib.testing.app.TestApp(__name__, set_as_current=True)
    app.conf['result_backend'] = 'redis+sync://{host}:{port}/{db}'.format(
        **redis_server.dsn())
    with celery.contrib.testing.app.setup_default_app(app), \
            celery.contrib.testing.worker.start_worker(app):
        yield app


# celery.contrib.testing.worker expects a 'ping' task, so it can check that the
# worker is running properly.
@celery.shared_task(name='celery.ping')
def celery_ping():
    return 'pong'
