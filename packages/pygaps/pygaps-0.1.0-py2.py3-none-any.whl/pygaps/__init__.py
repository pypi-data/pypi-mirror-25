# pylint: disable=W0614,W0401,W0611,W0622
# flake8: noqa

__author__ = 'Paul A. Iacomi'
__docformat__ = 'restructuredtext'
__doc__ = """
This module has many functionalities for manipulating
data from adsorption experiments

isort:skip_file
"""


# This code is written for Python 3.
import sys
if sys.version_info[0] != 3:
    print("Code requires Python 3.")
    sys.exit(1)


# Let users know if they're missing any of our hard dependencies
hard_dependencies = ("numpy", "pandas", "scipy",
                     "matplotlib", "sqlite3", "CoolProp")
missing_dependencies = []
dependency = None

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e_info:
        missing_dependencies.append(dependency)

if missing_dependencies:
    raise ImportError(
        "Missing required dependencies {0}".format(missing_dependencies))
del hard_dependencies, dependency, missing_dependencies

from pygaps.data import DATABASE
from pygaps.data import GAS_LIST
from pygaps.data import SAMPLE_LIST
from pygaps.api import *
