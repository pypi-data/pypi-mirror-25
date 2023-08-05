import os
import sys
from   setuptools import setup, find_packages
from   setuptools.command.test import test as TestCommand


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name="onyxjokes",
    version="0.0.6",
    author="Pyjokes Society",
    description="Add more language to Pyjokes by Pyjokes Society",
    license="BSD",
    keywords=[
        "pyjokes",
        "jokes",
        "onyxjokes",
        "onyx",
    ],
    url="https://github.com/pyjokes/pyjokes",
    packages=find_packages(),
    long_description=read('README.rst'),
    scripts=['scripts/onyxjoke',
             'scripts/onyxjokes'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
    ],
    #test requirements and class specification:
    tests_require=['pytest'],
    cmdclass={ 'test' : PyTest },
)
