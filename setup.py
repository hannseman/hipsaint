#!/usr/bin/env python
import os
from setuptools import setup, find_packages

version = __import__('hipsaint').__version__

setup(
    name             = "hipsaint",
    version          = version,

    description      = "",
    long_description = file(
        os.path.join(
            os.path.dirname(__file__),
            "README.md"
        )
    ).read(),
    author           = "Hannes Ljungberg",
    author_email     = "hannes@5monkeys.se",
    url              = "http://github.com/hannseman/hipsaint",
    download_url     = "https://github.com/5monkeys/hipsaint/tarball/%s" % (version,),

    keywords         = ["nagios", "hipchat", "api", "plugin"],
    classifiers      = [
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Utilities"
    ],

    zip_safe = False,
    packages = find_packages(exclude=["examples"]),
    include_package_data = True,

    install_requires = [
        "Jinja2==2.6",
        "requests==0.13.0"
    ],

    entry_points="""
    [console_scripts]
    hipsaint=hipsaint.bin.commands:main
	"""
)
