# coding=utf-8
from setuptools import setup, find_packages
from codecs import open
import os


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    return open(path, encoding='utf-8').read()


setup(
    name="Kool",
    version="0.0.2",
    packages=find_packages(),

    # development metadata
    zip_safe=False,

    # metadata for upload to PyPI
    author="Antony Orenge",
    author_email="orenge@ut.ee",
    description="Kool is an open source platform for online classroom management. ",
    license="MIT",
    keywords="education learning database nosql",
    url="https://github.com/edasi/kool",
    python_requires='>=3',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Education",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent"
    ],

    long_description=read('README.rst'),
)
