#!/usr/bin/env python

from setuptools import setup

_version = "2.2.1"


def read_files(*files):
    """Read files into setup"""
    text = ""
    for single_file in files:
        content = read(single_file)
        text = text + content + "\n"
    return text


def read(afile):
    """Read a file into setup"""
    with open(afile, 'r') as opened_file:
        content = filter_out_test_code(opened_file)
        content = "".join(list(content))
        return content


def filter_out_test_code(file_handle):
    found_test_code = False
    for line in file_handle.readlines():
        if line.startswith('.. testcode:'):
            found_test_code = True
            continue
        if found_test_code is True:
            if line.startswith('  '):
                continue
            else:
                empty_line = line.strip()
                if len(empty_line) == 0:
                    continue
                else:
                    found_test_code = False
                    yield line
        else:
            for keyword in ['|version|', '|today|']:
                if keyword in line:
                    break
            else:
                yield line


setup(
    name="excel2table",
    version=_version,
    description="Simple commandline utility to convert excel files"
    "to searchable and sortable HTML table.",
    author="Vivek R",
    author_email="vividvilla@gmail.com",
    maintainer="C. W.",
    maintainer_email="wangc_2011@hotmail.com",
    url="https://github.com/pyexcel/excel2table",
    packages=["excel2table"],
    include_package_data=True,
    long_description=read_files("README.rst", "CHANGELOG.rst"),
    download_url="https://github.com/pyexcel/excel2table/archive/{}.tar.gz"
        .format(_version),
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries"
    ],
    install_requires=["click >= 6.7", "jinja2 >= 2.9.6",
                      "pyexcel >= 0.5.0", "six >= 1.10.0",
                      "pyexcel-xls >= 0.4.0", "pyexcel-odsr >= 0.4.0"],
    entry_points={
        "console_scripts": [
            "excel2table = excel2table.cli:cli",
            ]
    }
)
