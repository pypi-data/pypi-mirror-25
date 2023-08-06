#!/usr/bin/env python

from setuptools import setup, find_packages

install_requires = [
    'requests==2.18.4',
]

tests_require = [
    'pytest',
    ]

setup(
    name='arm-python',
    version='0.1.0',
    author='Nikolay Donets',
    author_email='nd.startup@gmail.com',
    license='MIT',
    url='https://gitlab.com/nikdon/arm-python',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    description='The Python client for the Exeriments Platform API',
    download_url='https://gitlab.com/nikdon/arm-python/repository/0.1.0/archive.tar.gz',
    keywords=['client', 'api', 'wrapper'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)