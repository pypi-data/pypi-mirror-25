
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Don't import segmentio module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'segmentio'))
from version import VERSION

long_description = '''
Segment is the simplest way to integrate segmentio into your application.
One API allows you to turn on any other segmentio service. No more learning
new APIs, repeated code, and wasted development time.

This is a copy of the official library that renames the analytics module
segmentio.

This client wraps the the Segment REST API (https://segment.com).

Documentation and more details at https://github.com/jamiemccrindle/segmentio and
https://github.com/segmentio/analytics-python
'''

install_requires = [
    "requests>=2.7,<3.0",
    "six>=1.5",
    "python-dateutil>2.1"
]

setup(
    name='segmentio',
    version=VERSION,
    url='https://github.com/jamiemccrindle/segmentio',
    author='Not Segment',
    author_email='jamiemccrindle@gmail.com',
    maintainer='Segment',
    maintainer_email='jamiemccrindle@gmail.com',
    test_suite='segmentio.test.all',
    packages=['segmentio', 'segmentio.test'],
    license='MIT License',
    install_requires=install_requires,
    description='The hassle-free way to integrate analytics into any python application.',
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
