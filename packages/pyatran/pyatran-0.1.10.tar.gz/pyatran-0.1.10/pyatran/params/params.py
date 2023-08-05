# -*- coding: utf-8 -*-
from __future__ import unicode_literals, with_statement, division

"""
The mapping of the SCIATRAN parameters to JSON is as close to the original
control file structure as possible.

Example
-------

   {
       "control.inp": {
           "RTM Mode": "int",
           "RTM_TYPE": "ps_scat",
           "Verbosity level": "SS",
           "Advanced profile settings": "t"
       },
       "control_prof.inp": {
           "Trace gas replacement profiles": [
               [
                   "../data/profiles/camelot0_mozart_ext_alt.dat",
                   "O3",
                   "vmr",
                   2,
                   5
               ],
               [
                   "../data/profiles/camelot0_mozart_ext_alt.dat",
                   "NO2",
                   "vmr",
                   2,
                   6
               ]
           ]
       }
   }

"""


from collections import OrderedDict
import datetime
import json
import os

import numpy as np


try:
    class noquotestr(unicode):
        pass
except NameError:  # for Python3
    class noquotestr(str):
        pass

try:
    basestring = basestring
except NameError:
    basestring = (str, bytes)


def _prepare_val(v):
    """prepares a value for printing"""
    if isinstance(v, noquotestr):
        return "{}".format(v)
    if isinstance(v, basestring):
        if str(v) in ["t", "f"]:
            return v
        else:
            return "'{}'".format(v)
    elif isinstance(v, bool):
        return "t" if v else "f"
    elif isinstance(v, (datetime.date, datetime.datetime)):
        return v.strftime("%d.%m.%Y")
    elif np.issubdtype(v.__class__, int):
        return "{}".format(v)
    elif np.issubdtype(v.__class__, float):
        return "{}".format(v)
    else:
        raise ValueError('`v` is of class `{}`, and I don\'t know what to do'
                         ''.format(v.__class__))


def _prepare_list(l):
    """prepares a list for printing"""
    ret = []
    for i in l:
        ret.append(_prepare_val(i))
    return ",".join(ret) + "\n"


def json_to_sciatran(cfg, path):
    """Write SCIATRAN configuration.

    This function creates SCIATRAN parameter files in the directory
    ``path`` from the runtime configuration ``cfg``.

    Parameters
    ----------
    cfg : dict or str
       The SCIATRAN configuration to be written.  This can be either a
       Python dictionary or the filename of a JSON file holding
       SCIATRAN runtime configuration.

    path : str
       The directory in which the control files shall be written.

    """
    if isinstance(cfg, basestring):
        with open(cfg, "r") as fd:
            cfg = json.load(fd)
    for fn, subcfg in cfg.items():
        if not os.path.splitext(fn)[1].lower() == ".inp":
            continue
        with open(os.path.join(path, fn), "w") as fd:
            for key, val in subcfg.items():
                # some parameters must not be 'quoted'
                if key in ["Screen output", "Verbosity level",
                           "Retrieve profiles or columns?",
                           "Keep apriori information", "Surface type"]:
                    val = noquotestr(val)

                if key in ["Reference spectrum"] and isinstance(val, list):
                    for i, v in enumerate(val):
                        val[i] = noquotestr(v)

                # some params require additional info after the list length
                if key == "Spectral segment info":
                    extralistlen = ", 'nm'"
                else:
                    extralistlen = ""

                # brdf handling
                if key == "BRDF output control":
                    val = noquotestr("{}\n{}".format(_prepare_val(val[0]),
                                                     _prepare_val(val[1])))

                # wmo parameterization: composition of types
                if key == "Composition of aerosol types":
                    val = noquotestr(" " +
                                     "".join([_prepare_list(v) for v in val]))
                elif key == "Profile of extinction coefficient":
                    val = noquotestr("".join([_prepare_list(v) for v in val]))
                elif key == "Number of aerosol types and their names":
                    val = noquotestr("".join([_prepare_list(v) for v in val]))
                elif key == "Names aerosol types":
                    val = noquotestr("".join([_prepare_list(v) for v in val]))

                # manual parameterization: wavelength grid
                if key == "Number of wavelength and wavelength grid":
                    val = noquotestr("{}\n{}".format(len(val),
                                                     _prepare_list(val)))

                # in Retrieval mode, some parameters can be empty lists
                if key in ["Apriori information",
                           "Tikhonov parameter"] and len(val) == 0:
                    fd.write(key + "\n")
                    fd.write("0" + "\n\n")

                # Aerosol scattering matrix output
                elif key == "Aerosol scattering matrix output":
                    val = "{}\n{}{}".format(_prepare_val(val[0]),
                                            _prepare_list(val[1]),
                                            _prepare_val(val[2]))
                    fd.writelines("\n".join([key, val]) + u"\n\n")

                elif isinstance(val, list):
                    try:
                        if not isinstance(val[0], list):
                            fd.write(key + "\n")
                            fd.write(_prepare_list(val) + "\n")
                        elif key in ['Single scattering albedo',
                                     'Extinction coefficient']:
                            fd.write(key + "\n")
                            fd.writelines([_prepare_list(v) for v in val])
                            fd.write(u"\n")
                        else:
                            fd.writelines(key +
                                          u"\n{}{}\n".format(len(val),
                                                             extralistlen))
                            fd.writelines([_prepare_list(v) for v in val])
                            fd.write(u"\n")
                    except IndexError:
                        pass
                else:
                    fd.writelines("\n".join([key, _prepare_val(val)]) +
                                  u"\n\n")


def load_json(filename):
    """Load SCIATRAN configuration from JSON file.

    This function loads a SCIATRAN configuration from a JSON file.  No
    checking whatsoever of the validity of the file's contents is
    done.

    Parameters
    ----------
    filename : str

        File name of the JSON file holding the SCIATRAN configuration.

    Returns
    -------
    cfg : collections.OrderedDict
        The SCIATRAN configuration

    """
    with open(filename, "r") as fd:
        cfg = json.load(fd, object_pairs_hook=OrderedDict)
    return cfg
