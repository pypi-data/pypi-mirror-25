import os
from setuptools import setup, find_packages

__doc__ = """A python library for communicating with LimitlessLED/Milight/Easybulb compatible wifi bridges."""

setup(
    name="mookfist-lled-controller",
    description=__doc__,
    version="0.1.0",
    author="mookfist",
    author_email="mookfist@gmail.com",
    url="https://github.com/mookfist/mookfist-lled-controller",
    scripts=['lled.py'],
    packages=find_packages(),
    install_requires=[
        'docopt',
        'colorama',
        'sphinx_rtd_theme'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    keywords=['milight','limitlessled']
)
