import io
import os
import sys
import shutil
import subprocess
import setuptools

# read module version file
setup_abs_path = os.path.abspath(os.path.dirname(__file__))
version_abs_path = os.path.join(setup_abs_path, "mongobar", "__version__.py")
module_metadata = {}
with open(version_abs_path) as file_handle:
    exec(file_handle.read(), module_metadata)


setuptools.setup(
    name="mongobar",
    version=module_metadata["__version__"],
    description="MongoDB Backup and Restore Manager",
    keywords="mongodb backup restore mongodump mongorestore",
    url="https://github.com/chrisantonellis/mongobar",

    author="Christopher Antonellis",
    author_email="christopher.antonellis@gmail.com",
    license="MIT",
    packages=[
        "mongobar"
    ],
    # https://stackoverflow.com/a/5899643/1671562
    package_data={
        "mongobar": [
            "data/nouns.txt",
            "data/verbs.txt"
        ]
    },
    scripts=[
        "mongobar/scripts/mongobar"
    ],
    install_requires=[
        "pymongo",
        "colorama",
        "argcomplete",
        "terminaltables",
        "python-dateutil"
    ],
    extras_require={
        "tests": [
            "green",
            "coverage"
        ],
    }
)
