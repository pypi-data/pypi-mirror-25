import os
import re

from setuptools import find_packages, setup


def get_long_description():
    with open('README.rst', 'r') as f:
        return f.read()


def get_version(package):
    with open(os.path.join(package, '__init__.py')) as f:
        pattern = r'^__version__ = [\'"]([^\'"]*)[\'"]'
        return re.search(pattern, f.read(), re.MULTILINE).group(1)


setup(
    name='wola-sdk',
    version=get_version('wola_sdk'),
    description='Python SDK for Wola GraphQl',
    long_description=get_long_description(),
    author='mongkok',
    author_email='molina@waveapplication.com',
    maintainer='Wola',
    url='https://github.com/mongkok/wola-sdk/',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'gql>=0.1.0'
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    zip_safe=False,
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'gql>=0.1.0',
        'pytest>=3.0.7',
        'responses>=0.5.1'
    ]
)
