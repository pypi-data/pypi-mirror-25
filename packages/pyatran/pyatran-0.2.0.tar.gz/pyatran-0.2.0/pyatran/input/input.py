from __future__ import print_function, division, unicode_literals

from collections import OrderedDict
import copy
import os
import shutil
import warnings

import numpy as np


try:  # TODO there should be a more elegant way to do this ...
    isinstance('', basestring)
except NameError:
    basestring = str


__all__ = ["save_input_files"]


def mk_dirpath(name):
    return os.path.join('.', 'DATA_IN', name, '')


def _get_abspath(path, base):
    if os.path.isabs(path):
        abspath = path
    elif path.startswith("~"):
        abspath = os.path.expanduser(path)
    else:   # it's a relative path
        abspath = os.path.join(base, path)
    return abspath


def _copy_file(src, base, dst):
    assert os.path.isdir(dst)
    filename = os.path.split(src)[1]
    source = _get_abspath(src, base)
    target = os.path.abspath(os.path.join(dst, filename))
    if len(target) > 150:
        warnings.warn('The target path for copying {} is {}.  This is longer '
                      'than 150 characters, which might give problems with '
                      'SCIATRAN.'.format(filename, target))
    shutil.copy(source, target)
    # make target relative path
    path_components = dst.split(os.path.sep)
    ix_data_in = path_components.index('DATA_IN')
    target_dir = os.path.sep.join(path_components[ix_data_in:])
    target = os.path.join(target_dir, filename)
    if not target.startswith('.'):
        target = os.path.join('.', target)
    return target


def _save_input_files_xsectionsinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("xsections.inp")
    xsec_base = runcfg.get("X-section path")
    xsec_base = _get_abspath(xsec_base, base)
    if "Wavelength segment info" in cfg.get("control.inp").keys():
        wl_seg_info = cfg.get("control.inp").get("Wavelength segment info")
    else:
        wl_seg_info = cfg.get("control.inp").get("Spectral segment info")
    scia_min_wl = min([val[1] for val in wl_seg_info])
    scia_max_wl = max([val[2] for val in wl_seg_info])
    for k, v in runcfg.items():
        if not k.startswith("X-section: "):
            continue
        # for some configurations, not all xsections are needed
        if (k.startswith("X-section: o3_uv, ") and
                (scia_min_wl >= v[2] or scia_max_wl <= v[1])):
            continue
        if runcfg.get("Do O3 UV GOME FM") and k == "X-section: o3_uv, Bass":
            continue
        if (runcfg.get("Do O3 UV GOME FM") and scia_min_wl >= 235.1 and
                k == "X-section: o3 < 240 nm"):
            continue
        if (not runcfg.get("Do O3 UV GOME FM") and
                k == "X-section: o3_uv, GOME FM"):
            continue
        if (not runcfg.get("Do O3 UV GOME FM") and scia_min_wl >= 245.1 and
                k == "X-section: o3 < 240 nm"):
            continue
        # find out if there's more than one xsection for this trace gas
        if isinstance(v[0], list):
            for i, item in enumerate(v):
                _copy_file(v[i][0], xsec_base, dst)
        else:
            _copy_file(v[0], xsec_base, dst)
    # path should end with slash
    runcfg["X-section path"] = mk_dirpath('')
    return runcfg


def _save_input_files_controlinp(cfg, dst, base):
    if dst.find('DATA_IN') == -1:
        raise ValueError(
            'The `dst` needs to include the `DATA_IN` directory name`')
    if not dst.endswith(os.path.sep):
        dst = os.path.join(dst, '')
    runcfg = copy.deepcopy(cfg).get("control.inp")
    # Include land fluorescence
    key = "Include land fluorescence"
    val = runcfg.get(key)
    if val is not None:
        if isinstance(val, list):
            # rh-side of OR for compatibility with sciatran <v3.8.5
            if val[0] == 'file' or (isinstance(val[0], bool) and val[0]):
                runcfg[key][1] = _copy_file(val[1], base, dst)
    # Filename user provided solar spectrum
    if runcfg.get("Extra-terrestrial solar flux") == "File":
        key = "Filename user provided solar spectrum"
        val = runcfg.get(key)
        runcfg[key] = _copy_file(val, base, dst)
    # Wavelength grid from file
    key = "Wavelength grid from file"
    val = runcfg.get(key)
    if val is not None:
        if val[0]:
            runcfg[key][1] = _copy_file(val[1], base, dst)
    # Altitude grid file name
    key = "Altitude grid file name"
    val = runcfg.get(key)
    if val is not None:
        runcfg[key] = _copy_file(val, base, dst)
    # Standard profile scenario file name
    key = "Standard profile scenario file name"
    val = runcfg.get(key)
    if val is not None:
        runcfg[key] = _copy_file(val, base, dst)
    # Standard profile scenario file name for line absorbers
    key = "Standard profile scenario for line absorbers"
    val = runcfg.get(key)
    if val is not None:
        runcfg[key] = _copy_file(val, base, dst)
    # Spectral albedo filename
    if runcfg.get("Surface reflection type") == "alb_spec":
        key_file = "Spectral albedo filename"
        val_file = runcfg.get(key_file)
        key_dir = "Path to the albedo database"
        val_dir = runcfg.get(key_dir)
        fromfile = os.path.join(val_dir, val_file)
        _copy_file(fromfile, base, dst)
        runcfg[key_dir] = mk_dirpath('')
    # Replacement for water
    if runcfg.get("Surface reflection type") == "alb_db_mts":
        key_file = "Replacement for water"
        val_file = runcfg.get(key_file)
        key_dir = "Path to the albedo database"
        val_dir = runcfg.get(key_dir)
        fromfile = os.path.join(val_dir, val_file[1])
        _copy_file(fromfile, base, dst)
        runcfg[key_dir] = mk_dirpath('')
    # Collision-induced absorption
    runcfg["Path to CIA data base"] = mk_dirpath('')
    if runcfg.get("Collision-induced absorption") != "NONE":
        cia_base = runcfg.get("Path to CIA data base")
        cia_base = _get_abspath(cia_base, base)
        # TODO COPY CIA FILES
        raise NotImplementedError()
    runcfg["Path to climatology data base"] = mk_dirpath('')
    # TODO copy "Path to climatology data base"
    return runcfg


def _save_input_files_controlacinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("control_ac.inp")
    key = "Integration nodes"
    val = runcfg.get(key)
    if val is not None:
        if val[0]:
            runcfg[key][1] = _copy_file(val[1], base, dst)
    return runcfg


def _save_input_files_controlaerinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("control_aer.inp")
    key = "Path to Aerosol data base"
    val = runcfg.get(key)
    if val is not None:
        runcfg[key] = mk_dirpath('')
    return runcfg


def _save_input_files_controlgeominp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("control_geom.inp")
    return runcfg


def _save_input_files_controlprofinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("control_prof.inp")
    if runcfg.get("BrO climatology"):
        key = "BrO climatology file"
        val = runcfg.get(key)
        if val is not None:
            runcfg[key] = _copy_file(val, base, dst)
    if runcfg.get("Ozone climatology") != "NONE":
        runcfg["Path to ozone climatology"] = mk_dirpath('')
        # TODO: copy o3 climatology
        raise NotImplementedError()
        o3_base = runcfg.get("Path to ozone climatology")
        o3_base = _get_abspath(o3_base, base)
    if not runcfg.get("Do P and T from standard profile file"):
        key = "Pressure and temperature file name"
        val = runcfg.get(key)
        if val is not None:
            runcfg[key][0] = _copy_file(val[0], base, dst)
    profiles = runcfg.get("Trace gas replacement profiles")
    for i, prof in enumerate(profiles):
        runcfg["Trace gas replacement profiles"][i][0] = \
            _copy_file(prof[0], base, dst)
    runcfg["Use CIRA model"][1] = mk_dirpath('')
    # TODO copy files for "Use CIRA model"
    return runcfg


def _save_input_files_controlrayinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("control_ray.inp")
    if runcfg.get("King factor") == "from file":
        key = "Rayleigh depolarisation filename"
        val = runcfg.get(key)
        if val is not None:
            runcfg[key] = _copy_file(val, base, dst)
    return runcfg


def _save_input_files_controlrrsinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("control_rrs.inp")
    if runcfg.get("Use spin-rotational splitting")[0]:
        runcfg["Use spin-rotational splitting"][1] = _copy_file(
            runcfg["Use spin-rotational splitting"][1], base, dst)
        runcfg["Use spin-rotational splitting"][2] = _copy_file(
            runcfg["Use spin-rotational splitting"][2], base, dst)
    return runcfg


def _save_input_files_controlwfinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("control_wf.inp")
    return runcfg


def _save_input_files_controlretinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("control_ret.inp")

    # older versions of sciatran
    key = "Experimental data file"
    if key in runcfg:
        val = runcfg.get(key)
        runcfg[key] = _copy_file(val, base, dst)
    if "Reference spectrum" in runcfg:
        refspec = runcfg.get("Reference spectrum")
        if ((isinstance(refspec, basestring) and refspec == "sol") or
            (isinstance(refspec, list) and
             np.any([r == "sol" for r in refspec]))):
            key = "Solar spectrum file"
            val = runcfg.get(key)
            runcfg[key] = _copy_file(val, base, dst)
    if "Signal to Noise ratio mode" in runcfg:
        if runcfg.get("Signal to Noise ratio mode") == "R":
            key = "S/N ratio file"
            val = runcfg.get(key)
            runcfg[key] = _copy_file(val, base, dst)
    if "Number of correction spectra" in runcfg:
        if int(runcfg.get("Number of correction spectra")) > 0:
            corrspec_old = runcfg.get("Correction spectra file names and shift"
                                      " mode")
            corrspec_new = []
            assert int(runcfg.get("Number of correction "
                                  "spectra")) == len(corrspec_old)
            for fn, mod in runcfg.get("Correction spectra file names and shift"
                                      " mode"):
                corrspec_new.append(_copy_file(fn, base, dst), mod)

    return runcfg


def _save_input_files_controlbrdfinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("control_brdf.inp")
    # Coefficients of Ross-Li BRDF model
    if runcfg.get("Surface type") == "Ross-Li":
        key = "Coefficients of Ross-Li BRDF model"
        val = runcfg.get(key)
        runcfg[key] = _copy_file(val, base, dst)
    # Spherical albedo of vegetation and soil / Filename containing A/B coefficients  # noqa
    if runcfg.get("Surface type") == "svk":
        if not runcfg.get("Use A&B surface reflection database"):
            key = "Spherical albedo of vegetation and soil"
        else:
            key = "Filename containing A/B coefficients"
        val = runcfg.get(key)
        for i, f in enumerate(val):
            runcfg[key][i] = _copy_file(f, base, dst)
    # Filename (including path) containing model parameters
    if runcfg.get("Surface type") == "mRPV_facet":
        key = "Filename (including path) containing model parameters"
        val = runcfg.get(key)
        runcfg[key] = _copy_file(val, base, dst)
    # Filename containing BRDF
    if runcfg.get("Surface type") == "rff":
        key = "Filename containing BRDF"
        val = runcfg.get(key)
        runcfg[key] = _copy_file(val, base, dst)
    if runcfg.get("Surface type") == "ocean":
        # Transmission matrix water->air and air->water
        key = "Transmission matrix water->air and air->water"
        val = runcfg.get(key)
        for i, f in enumerate(val):
            runcfg[key][i] = _copy_file(f, base, dst)
        # Fresnel reflection
        if runcfg.get("Refractive index input type") == "wl_dep":
            key = "Refractive index file name"
            val = runcfg.get(key)
            runcfg[key] = _copy_file(val, base, dst)
        # reflectance emerging from sea water
        if runcfg["Whitecaps     Glint     Water leaving"][2] != "none":
            key = "Angular scattering coefficient filename"
            val = runcfg.get(key)
            runcfg[key] = _copy_file(val, base, dst)
            if runcfg["Absorption coefficients input type"] == "wl_dep":
                key = "Absorption coefficients file name"
                val = runcfg.get(key)
                runcfg[key] = _copy_file(val, base, dst)
    return runcfg


def _save_input_files_lowaerinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("low_aer.inp")
    aer_src = cfg.get("control_aer.inp").get("Path to aerosol data base")
    aer_src = os.path.join(aer_src, "LT")
    if cfg.get("control_aer.inp").get("Aerosol parameterization type") == "lt":
        aer_dst = os.path.join(dst, "LT")
        os.makedirs(aer_dst)
        _copy_file(os.path.join(aer_src, "DB_LT_WL.dat"), base, aer_dst)
        _copy_file(os.path.join(aer_src, "DB_PR.dat"), base, aer_dst)
        _copy_file(os.path.join(aer_src, "DBO_MS.dat"), base, aer_dst)
        _copy_file(os.path.join(aer_src, "DBO_ST.dat"), base, aer_dst)
        _copy_file(os.path.join(aer_src, "DBO_TR.dat"), base, aer_dst)
        bl_type = runcfg.get("Boundary layer aerosol type")
        if bl_type == 1:
            _copy_file(os.path.join(aer_src, "DBO_BL-rural.dat"),
                       base, aer_dst)
        elif bl_type == 2:
            _copy_file(os.path.join(aer_src, "DBO_BL-urban.dat"),
                       base, aer_dst)
        elif bl_type == 3:
            _copy_file(os.path.join(aer_src, "DBO_BL-maritime.dat"),
                       base, aer_dst,)
        else:   # bl_type == 4
            _copy_file(os.path.join(aer_src, "DBO_BL-tropospheric.dat"),
                       base, aer_dst)
    return runcfg


def _save_input_files_manaerinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("man_aer.inp")
    scatmat_base = runcfg.get("Directory name for scattering matrices")
    scatmat_base = _get_abspath(scatmat_base, base)
    if runcfg["Aerosol scattering function representation"] == "Expansion_coeff":  # noqa
        key = "File names containing expansion coefficients"
        val = runcfg.get(key)
        for i, alt in enumerate(val):
            for j, wl in enumerate(alt):
                runcfg[key][i][j] = _copy_file(wl, base, dst)
    if runcfg["Aerosol scattering function representation"] == "Scattering_matrix":  # noqa
        key = "File names containing scattering function/matrix"
        val = runcfg.get(key)
        for i, alt in enumerate(val):
            for j, wl in enumerate(alt):
                runcfg[key][i][j] = _copy_file(wl, base, dst)
    key = "Source for aerosol extinction coefficients"
    if runcfg[key] != "list":
        val = runcfg.get(key)
        for i, f in enumerate(val):
            runcfg[key][i] = _copy_file(f, base, dst)
    runcfg["Directory name for scattering matrices"] = mk_dirpath('')
    return runcfg


def _save_input_files_wmoaerinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("wmo_aer.inp")
    aer_src = cfg.get("control_aer.inp").get("Path to aerosol data base")
    aer_src = os.path.join(aer_src, "WMO")
    if cfg.get("control_aer.inp").get("Aerosol parameterization type") == "wm":
        aer_dst = os.path.join(dst, "WMO")
        os.makedirs(aer_dst)
        _copy_file(os.path.join(aer_src, "WMO_DB_WL_UV-TIR.dat"),
                   base, aer_dst)
        _copy_file(os.path.join(aer_src, "WMO_DB_MOM_UV-TIR.dat"),
                   base, aer_dst)
    return runcfg


def _save_input_files_wmogeninp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("wmo_general.inp")
    return runcfg


def _save_input_files_controloutinp(cfg, dst, base):
    runcfg = copy.deepcopy(cfg).get("control_out.inp")
    return runcfg


def save_input_files(cfg, path):
    """Copy SCIATRAN input files into runtime directory.

    This function scans the SCIATRAN configuration ``cfg`` for
    parameters which specify any input file *that is being used by the
    configuration*. These input files (e.g., cross-sections, profiles,
    ...) are then copied to the directory ``path/DATA_IN``, and the runtime
    configuration is adapted accordingly, to reflect the new directory
    structure.

    This function is meant to assist in creating independent SCIATRAN
    runtime directories which contain all the information needed to
    reproduce the run.

    Parameters
    ----------
    cfg : collections.OrderedDict
        The SCIATRAN configuration.

    path : str
        The directory where the input files shall be copied to.

    Returns
    -------
    runcfg : collections.OrderedDict
        The SCIATRAN configuration ``cfg``, but with the paths to all input
        files, which have been copied by this function to the folder
        ``path/DATA_IN``, updated so that they point to the input files within
        ``path/DATA_IN``.

    Notes
    -----
    - input files referenced indirectly in ``control.inp`` which are
      related to collision induced absorption are not treated yet
    - input files referenced indirectly in ``control_prof.inp`` which
      are related to the ozone climatologies are not treated yet

    Examples
    --------
    First, we need to load a SCIATRAN configuration from JSON:

    >>> cfg = pyatran.params.load_json('sciaconf.json')

    Say we want to copy all input files referenced in this configuration
    to the directory ``/path/to/DATA_IN``. Then, we would call this
    function as

    >>> runcfg = save_input_files(cfg, '/path/to')

    The configuration dict ``runcfg`` has the same contents as ``cfg``
    with the exception that the paths to all input files referenced in
    ``cfg`` have been updated to point to the input file's copy in
    ``/path/to/DATA_IN``.

    """
    # get base for any relative input paths
    if "base_directory" in cfg:
        base = os.path.abspath(cfg.get("base_directory"))
    else:
        base = os.getcwd()
    runcfg = OrderedDict()
    # path should end with slash
    target = os.path.abspath(os.path.join(path, "DATA_IN", ""))
    if not os.path.exists(target):
        os.makedirs(target)
    runcfg["control.inp"] = _save_input_files_controlinp(
        cfg, target, base)
    if "control_ac.inp" in cfg.keys():
        runcfg["control_ac.inp"] = _save_input_files_controlacinp(
            cfg, target, base)
    if "control_geom.inp" in cfg.keys():
        runcfg["control_geom.inp"] = _save_input_files_controlgeominp(
            cfg, target, base)
    if "control_prof.inp" in cfg.keys():
        runcfg["control_prof.inp"] = _save_input_files_controlprofinp(
            cfg, target, base)
    if "control_wf.inp" in cfg.keys():
        runcfg["control_wf.inp"] = _save_input_files_controlwfinp(
            cfg, target, base)
    if "man_aer.inp" in cfg.keys():
        runcfg["man_aer.inp"] = _save_input_files_manaerinp(
            cfg, target, base)
    if "low_aer.inp" in cfg.keys():
        runcfg["low_aer.inp"] = _save_input_files_lowaerinp(
            cfg, target, base)
    if "wmo_aer.inp" in cfg.keys():
        runcfg["wmo_aer.inp"] = _save_input_files_wmoaerinp(
            cfg, target, base)
    if "wmo_general.inp" in cfg.keys():
        runcfg["wmo_general.inp"] = _save_input_files_wmogeninp(
            cfg, target, base)
    if "control_brdf.inp" in cfg.keys():
        runcfg["control_brdf.inp"] = _save_input_files_controlbrdfinp(
            cfg, target, base)
    # control_aer has to come after low_aer etc.!!!
    if "control_aer.inp" in cfg.keys():
        runcfg["control_aer.inp"] = _save_input_files_controlaerinp(
            cfg, target, base)
    if "control_ret.inp" in cfg.keys():
        runcfg["control_ret.inp"] = _save_input_files_controlretinp(
            cfg, target, base)
    if "control_ray.inp" in cfg.keys():
        runcfg["control_ray.inp"] = _save_input_files_controlrayinp(
            cfg, target, base)
    if "control_rrs.inp" in cfg.keys():
        runcfg["control_rrs.inp"] = _save_input_files_controlrrsinp(
            cfg, target, base)
    runcfg["xsections.inp"] = _save_input_files_xsectionsinp(
        cfg, target, base)
    if "control_out.inp" in cfg.keys():
        runcfg["control_out.inp"] = _save_input_files_controloutinp(
            cfg, target, base)
    return runcfg
