from setuptools import setup

version = '0.0.3'
name = 'knapsack'
short_description = '`knapsack` is a package for for solving knapsack problem.'
long_description = """\
`knapsack` is a package for solving knapsack problem.
Maximize sum of selected weight.
Sum of selected size is les than capacity.
Algorithm: Dynamic Optimization
::

   import knapsack
   size = [21, 11, 15, 9, 34, 25, 41, 52]
   weight = [22, 12, 16, 10, 35, 26, 42, 53]
   capacity = 100
   knapsack.knapsack(size, weight).solve(capacity)

Requirements
------------
* Python 2 or Python 3

Features
--------
* nothing

Setup
-----
::

   $ pip install knapsack
   or
   $ easy_install knapsack

History
-------
0.0.1 (2015-6-26)
~~~~~~~~~~~~~~~~~~
* first release

"""

classifiers = [
   "Development Status :: 1 - Planning",
   "License :: OSI Approved :: Python Software Foundation License",
   "Programming Language :: Python",
   "Topic :: Software Development",
]

setup(
    name=name,
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=classifiers,
    py_modules=['knapsack'],
    keywords=['knapsack',],
    author='Saito Tsutomu',
    author_email='tsutomu@kke.co.jp',
    url='https://pypi.python.org/pypi/knapsack',
    license='PSFL',
)