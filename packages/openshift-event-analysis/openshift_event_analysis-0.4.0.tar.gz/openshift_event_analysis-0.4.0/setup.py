"""A setuptools based setup module for OpenShift Event Analytics.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='openshift_event_analysis',
    version='0.4.0',

    description='Some basic Classes to be use with OpenShift and Apache Kafka',
    long_description=long_description,

    url='https://gitlab.com/openshift-analytics/openshift_event_analysis',

    author='Christoph Görn',
    author_email='goern@redhat.com',

    license='GPLv3+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Other Environment',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='openshift kubernetes event_stream analysis',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['kafka', 'requests', 'prometheus_client'],

    extras_require={
        'dev': ['twine', 'check-manifest'],
        'test': ['coverage', 'flake8', 'pytest'],
    },

)
