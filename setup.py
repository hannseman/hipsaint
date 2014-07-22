#!/usr/bin/env python
from setuptools import setup, find_packages

version = __import__('hipsaint').__version__

setup(
    name="hipsaint",
    version=version,
    description="A command line tool for pushing Nagios host and service notifications to a HipChat room.",
    author="Hannes Ljungberg",
    author_email="hannes@5monkeys.se",
    url="http://github.com/hannseman/hipsaint",
    download_url="https://github.com/hannseman/hipsaint/tarball/%s" % (version,),
    keywords=["nagios", "hipchat", "api", "plugin"],
    license="WTFPL",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Environment :: Console",
        "Intended Audience :: Developers",
        'Intended Audience :: System Administrators',
        "Operating System :: OS Independent",
        "Topic :: Utilities"
    ],

    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    test_suite='hipsaint.tests',
    tests_require=['mock'],
    entry_points="""
    [console_scripts]
    hipsaint=hipsaint.bin.commands:main
    """
)
