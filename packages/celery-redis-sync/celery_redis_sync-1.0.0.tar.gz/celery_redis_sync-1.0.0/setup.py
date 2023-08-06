from setuptools import setup, find_packages


setup(
    name='celery_redis_sync',
    version='1.0.0',
    author='Zeit Online',
    author_email='zon-backend@zeit.de',
    url='https://github.com/zeitonline/celery_redis_sync',
    description="Synchronous Redis result store backend",
    long_description='\n\n'.join(
        open(x).read() for x in ['README.rst', 'CHANGES.txt']),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='BSD',
    install_requires=[
        'celery',
        'redis',
        'setuptools',
    ],
    extras_require={'test': [
        'mock',
        'pytest',
        'testing.redis',
    ]},
    entry_points={
        'celery.result_backends': [
            'redis = celery_redis_sync.redis_sync:select_backend'
        ],
    }
)
