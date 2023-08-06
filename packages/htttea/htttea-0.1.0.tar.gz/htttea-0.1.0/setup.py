#!/usr/bin/env python3
import os
import re
import setuptools
from typing import Dict


here = os.path.abspath(os.path.dirname(__file__))


def get_meta() -> Dict[str, str]:
    with open(os.path.join(here, 'htttea.py')) as f:
        source = f.read()

    regex = r'^{}\s*=\s*[\'"]([^\'"]*)[\'"]'
    return lambda name: re.search(regex.format(name), source, re.MULTILINE).group(1)


get_meta = get_meta()

with open(os.path.join(here, 'README.rst')) as f:
    readme = f.read()

install_requires = []

test_requires = [
    'Pygments',
    'docutils',
    'flake8',
    'mypy',
    'pytest',
    'pytest-cov',
    'requests',
]

setuptools.setup(
    name='htttea',
    version=get_meta('__version__'),
    description="Web server for testing.",
    long_description=readme,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries"
    ],
    keywords=["test", "http"],
    author=get_meta('__author__'),
    author_email=get_meta('__email__'),
    url="https://github.com/narusemotoki/htttea",
    license=get_meta('__license__'),
    py_modules=['htttea'],
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
    },
    include_package_data=True,
)
