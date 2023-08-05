# Python modules
from __future__ import division

# 3rd party modules

# Our modules
import chain_base


class ChainSpectralIdentity(chain_base.Chain):
    # FIXME PS docstring
    def __init__(self, dataset, block):
        """ Prepare the base class. """
        chain_base.Chain.__init__(self, dataset, block)

        
