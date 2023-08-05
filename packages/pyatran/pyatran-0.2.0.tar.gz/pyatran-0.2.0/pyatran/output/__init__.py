# -*- coding: utf-8 -*-

"""pyatran.output
=================

Reading SCIATRAN output from the ``DATA_OUT`` directory into pandas
data structures.

.. autosummary::
   :toctree: api/

   read_sciatran_output
   read_inp_par
   read_xsection_data
   Result

"""

from .output import Result
from .read_sciatran import read_sciatran_output
from .read_inp_pars import read_inp_par, read_xsection_data
