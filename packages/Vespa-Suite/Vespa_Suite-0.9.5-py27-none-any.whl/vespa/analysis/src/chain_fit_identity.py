# Python modules
from __future__ import division

# 3rd party modules
import numpy as np

# Our modules
import constants
import chain_base


class ChainFitIdentity(chain_base.Chain):
    # FIXME PS docstring
    def __init__(self, dataset, block):
        """ Prepare the base class. """
        chain_base.Chain.__init__(self, dataset, block)

