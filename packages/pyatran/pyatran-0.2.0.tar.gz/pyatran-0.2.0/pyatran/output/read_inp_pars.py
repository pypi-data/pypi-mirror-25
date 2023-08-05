import os.path
import re

import numpy as np
import pandas as pd
import xarray as xr


def sanitize_single_param(p):
    """Sanitize a single parameter

    Parameters
    ----------
    p : str
        The parameter to sanitize

    Returns
    -------
    sanitized : str or int or float

    Examples
    --------

    >>> sanitize_single_param('t')
    True

    >>> sanitize_single_param('"This is a string"')
    'This is a string'

    >>> sanitize_single_param('293.0')
    293.0

    """
    if p.lower() == 't':
        return True
    if p.lower() == 'f':
        return False
    for quotechar in ['"', '\'']:
        if (p.count(quotechar) == 2 and p.startswith(quotechar) and
                p.endswith(quotechar)):
            return p[1:-1]
    if p.count('.') == 0:
        try:
            return int(p)
        except ValueError:
            pass
    try:
        return float(p)
    except ValueError:
        pass
    return p


def read_inp_par(fn, par):
    """Read one parameter from ``SCE_INP_PARS.OUT``

    This function reads the value of a single parameter from a SCIATRAN
    ``SCE_INP_PARS.OUT`` file.  The parameter value(s) will be sanitized,
    i.e., converted to list, float, int, str objects.

    Parameters
    ----------
    fn : str
        Path to the file to read

    par : str
        Parameter to read from the file

    Returns
    -------
    parvals : list or single parameter

    """
    with open(fn, 'r') as fd:
        inpfile = fd.readlines()
    parvals = []
    curpar = ''
    for line in inpfile:
        if line.strip().startswith('***'):  # new parameter
            if curpar == par:  # if we are at the requested par, return
                if len(parvals) == 0:
                    return
                elif len(parvals) == 1:
                    return parvals[0]
                else:
                    return parvals
            curpar = line.split('***')[1].strip()
            parvals = []
        elif curpar == par:  # we're reading the requested param
            thispar = line.split('-->')[1].strip()
            # split line at ',' see https://stackoverflow.com/a/16710842/152439
            thispar = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', thispar)
            thispar = [sanitize_single_param(t) for t in thispar]
            thispar = thispar[0] if len(thispar) == 1 else thispar
            if thispar == []:
                thispar = None
            parvals.append(thispar)
    if len(parvals) == 0:
        raise ValueError(
            'Could not find parameter "{}" in file {}'.format(par, fn))
    elif len(parvals) == 1:
        return parvals[0]
    else:
        return parvals


def read_xsection_filenames(fn):
    with open(fn, 'r') as fd:
        inpfile = fd.readlines()

    # sanitize input file
    inpfile = [l.strip() for l in inpfile]

    # find all keys
    keys = [l.split('***')[1].strip() for l in inpfile
            if l.startswith('***')]

    # find all xsection keys
    xsection_keys = [k.split(':')[1].strip() for k in keys
                     if k.startswith('X-section:')]

    # read xsection info
    xsections = {}
    for k in xsection_keys:
        val = read_inp_par(fn, 'X-section: {}'.format(k))
        xsections[k] = val
        if k not in ['o3_uv, Bass']:
            xsections[k] = xsections[k][1:]

    # fix full paths to xsection files
    path = read_inp_par(fn, 'X-section path')
    for k, v in xsections.items():
        if k in ['o3_uv, Bass']:
            xsections[k][0] = os.path.join(path, xsections[k][0])
            continue
        for i, x in enumerate(v):
            xsections[k][i][0] = os.path.join(path, xsections[k][i][0])
    return xsections


def read_xsection_data(fn_pars):
    """Read SCIATRAN input cross-sections

    This function reads all cross-sections which have been used in a SCIATRAN
    simulation.  The filenames and temperatures are being read from the
    ``SCE_INP_PARS.OUT`` file from SCIATRAN's ``DATA_OUT`` directory.

    Parameters
    ----------
    fn_pars : str
        Path to the ``SCE_INP_PARS.OUT`` file from which the cross-section
        filenames shall be read.

    Returns
    -------
    xs : xarray.Dataset
        The cross-section data.

    """
    fileinfo = read_xsection_filenames(fn_pars)
    xs = {}
    for k, v in fileinfo.items():
        if k in ['o3_uv, Bass']:
            continue  # TODO what should we do with this one?
        temps = sorted([t for fn, t in v])
        fn, t = v[0]
        kshort = 'o3' if k == 'o3 UV-NIR' else k

        wl_arr = pd.read_csv(
            fn, comment='#', delim_whitespace=True, header=None)
        wl = wl_arr.values[:, 0]
        xs_tmp = xr.DataArray(
            np.empty((len(temps), wl.size)),
            {'temperature_xsection_{}'.format(kshort): temps,
             'wavelength_xsection_{}'.format(kshort): wl},
            ['temperature_xsection_{}'.format(kshort),
             'wavelength_xsection_{}'.format(kshort)])
        for fn, t in v:
            d = pd.read_csv(
                fn, comment='#', delim_whitespace=True, header=None)
            xs_tmp.loc[t] = d.values[:, 1]

        k = kshort
        xs['xsection_{}'.format(k)] = xs_tmp

    return xr.Dataset(xs)
