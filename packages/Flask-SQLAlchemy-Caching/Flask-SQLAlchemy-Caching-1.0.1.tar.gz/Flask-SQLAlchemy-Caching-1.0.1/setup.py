#!/usr/bin/env python

from setuptools import setup

setup(
    name='Flask-SQLAlchemy-Caching',
    version='1.0.1',
    description='CachingQuery implementation to Flask using Flask-SQLAlchemy and Flask-Caching',
    author='Brad Belyeu',
    author_email='developers@youversion.com',
    url='http://www.github.com/youversion/Flask-SQLAlchemy-Caching',
    download_url='https://github.com/youversion/Flask-SQLAlchemy-Caching/archive/1.0.1.zip',
    license='MIT',
    platforms='any',
    packages=['flask_sqlalchemy_caching'],
    install_requires=[
        'Flask>=0.12.2',
        'Flask-Caching>=1.3.2',
        'Flask-SQLAlchemy>=2.2',
    ],
    test_suite='flask_sqlalchemy_caching.tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['flask', 'sqlalchemy', 'caching', 'cache'],
)
