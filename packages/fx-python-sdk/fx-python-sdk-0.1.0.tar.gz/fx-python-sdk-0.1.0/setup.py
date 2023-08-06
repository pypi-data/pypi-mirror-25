import os
import platform
import re
import sys
from distutils.command.build_ext import build_ext
from distutils.errors import DistutilsExecError
from distutils.errors import DistutilsPlatformError
from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand

VERSION = "0.1.0"

cmdclass = {}
if sys.version_info < (2, 7):
    raise Exception("Python 2.7 is required.")
if sys.version_info > (3, 0):
    raise Exception("Python 3 not supported at this time.")

class PyTest(TestCommand):
    # from http://pytest.org/latest/goodpractices.html\
    # #integrating-with-setuptools-python-setup-py-test-pytest-runner
    # TODO: prefer pytest-runner package at some point, however it was
    # not working at the time of this comment.
    user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

    default_options = ["-n", "4", "-q"]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren"t loaded
        import pytest
        errno = pytest.main(self.default_options + shlex.split(self.pytest_args))
        sys.exit(errno)

cmdclass["test"] = PyTest


def run_setup():
    setup(
        name="fx-python-sdk",
        version=VERSION,
        description="Python SDK for Impossible FX",
        author="Impossible Software",
        author_email="gh@impossiblesoftware.com",
        url="https://www.impossiblesoftware.com/",
        packages=["impossible_fx"],
        license="MIT License",
        cmdclass=cmdclass,
        tests_require=["pytest >= 2.5.2"],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Topic :: Multimedia :: Video"
        ],
        install_requires=[
            "requests",
            "protobuf",
        ]
    )

if __name__ == "__main__":
    run_setup()
