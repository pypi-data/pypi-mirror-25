import io
import os
import sys
import shutil
import subprocess
import setuptools


# read module version file
setup_abs_path = os.path.abspath(os.path.dirname(__file__))
version_abs_path = os.path.join(setup_abs_path, "delimited", "__version__.py")
module_metadata = {}
with open(version_abs_path) as file_handle:
    exec(file_handle.read(), module_metadata)


setuptools.setup(
    name="delimited",
    version=module_metadata["__version__"],
    description="delimited defines types that allow for accessing and modifying nested data by delimited string",
    keywords="delimited nested",
    url="https://github.com/chrisantonellis/delimited",

    author="Christopher Antonellis",
    author_email="christopher.antonellis@gmail.com",
    license="MIT",
    packages=[
        "delimited"
    ],
    extras_require={
        "tests": [
            "green",
            "coverage"
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha"
    ]
)
