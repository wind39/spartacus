"""
The MIT License (MIT)

Copyright (c) 2014-2019 William Ivanski
Copyright (c) 2018-2019 Israel Barth Rubio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
from setuptools import setup

rootdir = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(rootdir, "README")).read()

setup(
    name="Spartacus",
    version="3.37",
    description="Generic database wrapper",
    long_description=long_description,
    url="http://github.com/wind39/spartacus",
    author="William Ivanski",
    author_email="william.ivanski@gmail.com",
    license="MIT",
    packages=["Spartacus"],
    install_requires=[
        "pyscrypt",
        "pyaes",
        "click",
        "sqlparse",
        "tabulate",
        "cryptography",
    ],
    extras_require={
        "postgresql": ["psycopg2-binary", "pgspecial"],
        "mysql": ["PyMySQL"],
        "mariadb": ["PyMySQL"],
        "firebird": ["fdb"],
        "oracle": ["cx_Oracle"],
        "mssql": ["pymssql"],
        "ibmdb2": ["ibm_db"],
        "xlsx": ["openpyxl", "bs4", "lxml", "Pillow"],
        "xls": ["openpyxl", "bs4", "lxml", "Pillow", "pyexcel", "pyexcel-xlsx", "pyexcel-xls"],
        "complete": [
            "psycopg2-binary",
            "pgspecial",
            "PyMySQL",
            "fdb",
            "cx_Oracle",
            "pymssql",
            "ibm_db",
            "openpyxl",
            "bs4",
            "lxml",
            "Pillow",
            "pyexcel",
            "pyexcel-xlsx",
            "pyexcel-xls"
        ],
    },
    zip_safe=False,
)
