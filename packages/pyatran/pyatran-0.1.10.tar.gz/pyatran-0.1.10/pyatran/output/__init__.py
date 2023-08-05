# -*- coding: utf-8 -*-

"""pyatran.output
=================

Reading SCIATRAN output from the ``DATA_OUT`` directory into pandas
data structures.

.. autosummary::
   :toctree: api/

   read_sciatran_output
   Result

"""

from .output import Result
from .read_sciatran import read_sciatran_output
