#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io
import sys

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
    long_description = readme.read()

needs_wheel = {'release', 'bdist_wheel', 'dists'}.intersection(sys.argv)
wheel = ['wheel'] if needs_wheel else []

name = 'vr.server'
description = 'Velociraptor\'s Django and Celery components.'

setup_params = dict(
    name=name,
    use_scm_version=True,
    author="Brent Tubbs",
    author_email="btubbs@gmail.com",
    description=description or name,
    long_description=long_description,
    url="https://github.com/yougov/" + name,
    packages=setuptools.find_packages(),
    include_package_data=True,
    namespace_packages=name.split('.')[:-1],
    install_requires=[
        'celery-schedulers==0.0.2',
        'diff-match-patch==20121119',
        'Django>=1.8,<1.9',
        'django-celery>=3.1.17,<3.2',
        'django-extensions==1.5.9',
        'django-picklefield==0.2.0',
        'django-redis-cache==0.9.5',
        'django-reversion==1.9.3',
        'django-tastypie==0.12.2',
        'Fabric3bis',
        'gevent>=1.1rc1,<2',
        'psycogreen',
        'gunicorn==0.17.2',
        'paramiko>=1.15.3,<2.0',
        'psycopg2>=2.4.4,<2.5',
        'pymongo>=2.5.2,<4',
        'redis>=2.6.2,<3',
        'requests>=2.11.1',
        'setproctitle',
        'sseclient==0.0.11',
        'six>=1.4',
        'vr.events>=1.2.1',
        'vr.common>=4.9.3',
        'vr.builder>=1.3',
        'vr.imager>=1.3',
        'django-yamlfield',
        'backports.functools_lru_cache',
        # Celery 4 removes support for e-mail
        # https://github.com/celery/celery/blob/master/docs/whatsnew-4.0.rst#removed-features
        'celery<4dev',
        'jaraco.functools',
    ],
    extras_require={
        ':python_version=="2.7"': [
            'mercurial>=3.8',
        ],
    },
    setup_requires=[
        'setuptools_scm>=1.15.0',
    ] + wheel,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
    ],
    entry_points={
        'console_scripts': [
            'vr_worker = vr.server.commands:start_celery',
            'vr_beat = vr.server.commands:start_celerybeat',
            'vr_migrate = vr.server.commands:run_migrations',
        ],
    },
)
if __name__ == '__main__':
    setuptools.setup(**setup_params)
