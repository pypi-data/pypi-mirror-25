# -*- coding: utf-8 -*-

"""
Pythonic class collection that helps you structure external data from LHC / HEP experiments.
"""


__author__     = "Marcel Rieger"
__email__      = "python-order@googlegroups.com"
__copyright__  = "Copyright 2017, Marcel Rieger"
__credits__    = ["Marcel Rieger"]
__contact__    = "https://github.com/riga/order"
__license__    = "MIT"
__status__     = "Development"
__version__    = "0.1.1"

__all__ = ["UniqueObject", "UniqueObjectIndex", "uniqueness_context", "CopyMixin", "AuxDataMixin",
           "TagMixin", "DataSourceMixin", "SelectionMixin", "LabelMixin", "ColorMixin", "Channel",
           "Category", "Variable", "Shift", "Process", "Dataset", "DatasetInfo", "Campaign",
           "Config", "Analysis", "cms"]


# provisioning imports
from .unique import UniqueObject, UniqueObjectIndex, uniqueness_context
from .mixins import CopyMixin, AuxDataMixin, TagMixin, DataSourceMixin, SelectionMixin, \
    LabelMixin, ColorMixin
from .categorize import Channel, Category
from .variable import Variable
from .shift import Shift
from .process import Process
from .dataset import Dataset, DatasetInfo
from .config import Campaign, Config
from .analysis import Analysis

# submodules
from . import cms
