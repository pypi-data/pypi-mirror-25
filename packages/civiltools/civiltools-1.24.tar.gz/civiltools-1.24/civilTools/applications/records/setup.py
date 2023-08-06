#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


#with open('README.rst') as readme_file:
    #readme = readme_file.read()

#with open('HISTORY.rst') as history_file:
    #history = history_file.read()

requirements = [
'alabaster>=0.7.10',
'appdirs>=1.4.3',
'arrow>=0.10.0',
'Babel>=2.4.0',
'binaryornot>=0.4.0',
'chardet>=2.3.0',
'click>=6.7',
'cycler>=0.10.0',
'docutils>=0.13.1',
'earthquakerecords>=0.1.0',
'future>=0.16.0',
'imagesize>=0.7.1',
'Jinja2>=2.9.5',
'jinja2-time>=0.2.0',
'MarkupSafe>=1.0',
'matplotlib>=2.0.0',
'numpy>=1.12.1',
'packaging>=16.8',
'pandas>=0.19.2',
'poyo>=0.4.1',
'py>=1.4.33',
'Pygments>=2.2.0',
'pyparsing>=2.2.0',
'PyQt5>=5.8.1',
'pyqtgraph>=0.10.0',
'pytest>=3.0.7',
'pytest-cov>=2.4.0',
'python-dateutil>=2.6.0',
'pytz>=2016.10',
'requests>=2.13.0',
'scipy>=0.19.0',
'sip>=4.19.1',
'six>=1.10.0',
'snowballstemmer>=1.2.1',
'Sphinx>=1.5.3',
'whichcraft>=0.4.0',

]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='earthquakerecords',
    version='0.1.4',
    description="A series of tools for civil engineers.",
    long_description='',
    author="Raeyat Ebrahim",
    author_email='ebe79442114@yahoo.com',
    url='https://github.com/ebrahimraeyat/civiltools',
    packages=[
        'records',
    ],
    package_dir={'records':
                 'records'},
    include_package_data=True,
    install_requires=requirements,
    license="GPL",
    zip_safe=False,
    keywords='civiltools',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)


#from __future__ import print_function
#from setuptools import setup, find_packages
#from setuptools.command.test import test as TestCommand
#import io
#import codecs
#import os
#import sys

#import records

#here = os.path.abspath(os.path.dirname(__file__))

#def read(*filenames, **kwargs):
    #encoding = kwargs.get('encoding', 'utf-8')
    #sep = kwargs.get('sep', '\n')
    #buf = []
    #for filename in filenames:
        #with io.open(filename, encoding=encoding) as f:
            #buf.append(f.read())
    #return sep.join(buf)

#long_description = read('README.txt', 'CHANGES.txt')

#class PyTest(TestCommand):
    #def finalize_options(self):
        #TestCommand.finalize_options(self)
        #self.test_args = []
        #self.test_suite = True

    #def run_tests(self):
        #import pytest
        #errcode = pytest.main(self.test_args)
        #sys.exit(errcode)

#setup(
    #name='sandman',
    #version=records.__version__,
    #url='http://github.com/jeffknupp/sandman/',
    #license='Apache Software License',
    #author='Jeff Knupp',
    #tests_require=['pytest'],
    #install_requires=['Flask>=0.10.1',
                    #'Flask-SQLAlchemy>=1.0',
                    #'SQLAlchemy==0.8.2',
                    #],
    #cmdclass={'test': PyTest},
    #author_email='jeff@jeffknupp.com',
    #description='Automated REST APIs for existing database-driven systems',
    #long_description=long_description,
    #packages=['sandman'],
    #include_package_data=True,
    #platforms='any',
    #test_suite='sandman.test.test_sandman',
    #classifiers = [
        #'Programming Language :: Python',
        #'Development Status :: 4 - Beta',
        #'Natural Language :: English',
        #'Environment :: Web Environment',
        #'Intended Audience :: Developers',
        #'License :: OSI Approved :: Apache Software License',
        #'Operating System :: OS Independent',
        #'Topic :: Software Development :: Libraries :: Python Modules',
        #'Topic :: Software Development :: Libraries :: Application Frameworks',
        #'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        #],
    #extras_require={
        #'testing': ['pytest'],
    #}
#)
