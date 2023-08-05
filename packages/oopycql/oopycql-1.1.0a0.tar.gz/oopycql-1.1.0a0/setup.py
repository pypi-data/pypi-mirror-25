"""
OOPyCQL
-------------

An object oritneted interface for the Cypher Query Language in Python.
"""
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

append_to_deps = []
try:
    from functools import lru_cache
    del lru_cache
except ImportError:
    append_to_deps.append('functools32')

if sys.version_info.major < 3 or sys.version_info.minor < 4:
    append_to_deps.append('pathlib')

__author__ = 'Dom Weldon <dom.weldon@gmail.com>'
__email__ = 'dom.weldon@gmail.com'
__license__ = 'Apache License, Version 2.0'
__package__ = 'oopycql'
__version__ = '1.1.0a0'

required_deps = [
    'six',
    'regex',
] + append_to_deps


setup(
    name='oopycql',
    version=__version__,
    url='https://github.com/DomWeldon/oopycql',
    license='Apache License, Version 2.0',
    author='Dom Weldon',
    author_email='dom.weldon@gmail.com',
    description='An object oritneted interface for the cypher query language',
    long_description=__doc__,
    packages=['oopycql'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=required_deps,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Database",
    ],
    keywords='graph database neo4j cypher cql',
    test_suite='py.test',
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
    python_requires='>=2.7',
    download_url='https://github.com/domweldon/oopycql/archive/0.1.0.tar.gz'
)
