#!/usr/bin/env python
import codecs

from setuptools import setup
from setuptools import find_packages


VERSION = (0, 1, 6)
SEPARATOR = '.'


def get_version():
    return SEPARATOR.join(map(lambda x: str(x), VERSION))

__version__ = get_version()


def parse(*args, **kwargs):
    """
    Parse documentation files into internal variable for rendering with setup
    """
    # noinspection PyPep8Naming
    SEPARATOR = kwargs.get('separator', '\n')
    coding = kwargs.get('coding', 'UTF-8')
    stream = []

    for arg in args:
        with codecs.open(arg, 'r', coding) as document:
            stream.append(document.read())

    return SEPARATOR.join(stream)


#: LONG_DESCRIPTION = parse('README.rst')

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Utilities",
    "Topic :: Software Development"
]


setup(
    name='geocsvlib',
    description='IP Geolocation data CSV Parser Library',
    url='http://github.com/rayattack/geocsvlib',
    version=__version__,
    license='MIT',
    author='Raymond Ortserga',
    author_email='ortserga@yahoo.com',
    zip_safe=False,
    packages=find_packages(),
    install_requires=['mongoengine'],
    keywords='IP Location Parser CSV',
    classifiers=CLASSIFIERS,
    long_description="",
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=['geocsvlib/geocsv']
)
