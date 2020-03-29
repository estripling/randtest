"""Packaging settings"""

from pathlib import Path
from setuptools import setup, find_packages


from randtest import (
    __author__,
    __email__,
    __version__,
)


base_directory = Path(__file__).parent.resolve()
long_desc = base_directory.joinpath("README.md").read_text()


setup(
    name="randtest",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="Randomization tests for two-sample comparison.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/estripling/randtest",
    python_requires=">= 3.7",
    packages=find_packages(),
    license="MIT",
    entry_points={
        "console_scripts": [
            "randtest-mean = randtest.randtest_mean:main",
            "randtest-tmean = randtest.randtest_tmean:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
