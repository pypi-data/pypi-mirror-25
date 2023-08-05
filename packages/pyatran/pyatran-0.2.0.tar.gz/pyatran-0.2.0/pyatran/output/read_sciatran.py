from distutils.version import LooseVersion
from glob import glob
import os.path
import shutil
import tarfile
import tempfile
import warnings
import zipfile

import numpy as np
import pandas as pd
import xarray as xr

import pyatran
from pyatran.output.read_inp_pars import read_inp_par


try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


STANDARD_NAMES = {
    'altitude': 'altitude',
    'air_pressure': 'air_pressure',
    'air_temperature': 'air_temperature',
    'air_density': 'air_density',
}

UNITS = {
    # all other variables will have units of 'molec cm-3'
    'altitude': 'km',
    'air_pressure': 'hPa',
    'air_temperature': 'K',
}

SPECIES_STANDARD_NAMES = {
    'bro': 'bromine_monoxide',
    'chocho': 'glyoxal',
    'oclo': 'chlorine_dioxide',
    'no': 'nitrogen_oxide',
    'no2': 'nitrogen_dioxide',
    'no3': 'nitrate',
    'o3': 'ozone',
    'hcho': 'formaldehyde',
    'ch4': 'methane',
    'co': 'carbon_monoxide',
    'co2': 'carbon_dioxide',
    'hono': 'nitrous_acid',
}


def rename_species(dataset, new_names):
    """Rename a species in an output Dataset

    Sometimes, it is necessary to use a fake species name instead of the
    correct one in SCIATRAN.  For example, SCIATRAN doesn't know about glyoxal.

    Parameters
    ----------
    dataset : xarray.Dataset
        The dataset containing the SCIATRAN output with the 'fake' species
        names

    new_names : dict
        A dictionary ``{old_name: new_name}``

    Returns
    -------
    dataset_new : xarray.Dataset
        The dataset with the species names replaced

    """
    for old, new in new_names.items():
        vars_to_change = [var for var in dataset.data_vars
                          if var.endswith('_{}'.format(old))]
        stdname_old = SPECIES_STANDARD_NAMES[old]
        stdname_new = SPECIES_STANDARD_NAMES[new]
        for var in vars_to_change:
            for k, v in dataset[var].attrs.items():
                dataset[var].attrs[k] = dataset[var].attrs[k].replace(
                    stdname_old, stdname_new)
            dataset.rename({var: var.replace(old, new)}, inplace=True)
    return dataset


def _get_rt_mode(fn):
    """Reads the RT-Mode from SCIATRAN output.

    Parameters
    ----------
    fn : str
        Path to the ``DATA_OUT`` directory

    Returns
    -------
    mode : str
        One of ``DOM-S``, ``CDI``, and ``DOM-V``

    """

    with open(fn, "r") as fd:
        mode = None
        for line in fd:
            if line.find("scalar RT") > -1:
                mode = "DOM-S"
            elif line.find("vector RT") > -1:
                mode = "DOM-V"
            elif line.find("CDI, ") > -1:
                mode = "CDI"
    if mode is None:
        raise ValueError("Cannot determine RT type from "
                         "'{}'".format(os.path.split(fn)[1]))
    return mode


def _get_absorber_name_from_header(fn):
    """Reads the absorber name from SCIATRAN output file header.

    Notes
    -----

    Currently, the following output files are supported:

    - ``slant_col.dat``
    - ``vert_col.dat``
    - ``block_amf.dat``
    - ``.dat``

    The following SCIATRAN output files do not contain information on the
    absorber:

    - ``wf_XXX.dat``

    """
    with open(fn, 'r') as fd:
        lines = fd.readlines()
    header = [l for l in lines if l.startswith('#')]
    for h in header:
        for id_string in ['vertical colums for', 'vertical columns for']:
            test_vcd = h.lower().split(id_string)
            if len(test_vcd) > 1:
                return test_vcd[1].strip()
        for id_string in ['slant colums for', 'slant columns for']:
            test_scd = h.lower().split(id_string)
            if len(test_scd) > 1:
                return test_scd[1].strip()
        for id_string in ['Height resolved air mass factors for']:
            test_bamf = h.lower().split(id_string)
            if len(test_bamf) > 1:
                return test_bamf[1].strip()
    raise ValueError


def read_sce_absorber(fn):
    """Read an ``SCE_ABSORBER.OUT`` file from SCIATRAN

    Parameters
    ----------
    fn : str
        Path to the output_map file

    Returns
    -------
    sce_absorber : xarray.Dataset
        All information contained in the ``SCE_ABSORBER.OUT`` file.

    """
    with open(fn, "r") as fd:
        nameline = fd.readlines()[9]
        names = nameline.split()
    try:
        idx_Air = names.index("Air")
        if names[idx_Air + 1] == "dens":
            names[idx_Air] = "Airdens"
            names.pop(idx_Air + 1)
    except ValueError:
        pass

    # find out which lines to read
    with open(fn, "r") as fd:
        lines = fd.readlines()
    n_skipheader, n_skipfooter = -1, -1
    for ii, l in enumerate(lines):
        if l.strip().startswith('----------------------'):
            if n_skipheader == -1:
                n_skipheader = ii + 1
            elif n_skipfooter == -1:
                n_skipfooter = len(lines) - ii
            else:
                raise ValueError
    assert n_skipheader != -1 and n_skipfooter != -1

    # read profile data
    data = pd.read_csv(fn, sep=str(r"\s+"), skipinitialspace=True,
                       header=None, index_col=0, engine="python",
                       skiprows=n_skipheader, skipfooter=n_skipfooter)
    # read_csv adds empty column at end; we remove it here
    if data.iloc[:, -1].dropna().shape == (0, ):
        data.drop(data.columns[-1], axis=1, inplace=True)
    try:
        data.columns = names[1:]
    except:
        raise ValueError("Something's wrong here.")

    data.index.name = 'layer'
    ds = xr.Dataset.from_dataframe(data)
    ds.rename({'Z': 'altitude', 'P': 'air_pressure', 'T': 'air_temperature',
               'Airdens': 'air_density'},
              inplace=True)
    absorber_list = [dv for dv in ds.data_vars
                     if dv not in ['altitude', 'air_pressure',
                                   'air_temperature', 'air_density']]
    ds.rename({absorber: 'profile_{}'.format(absorber)
               for absorber in absorber_list},
              inplace=True)

    for var in ds.data_vars:
        absorber = var.split('profile_')[-1]
        absorber_stdname = SPECIES_STANDARD_NAMES.get(absorber, absorber)
        ds[var].attrs['standard_name'] = STANDARD_NAMES.get(
            var, 'number_concentration_of_{}_in_air'.format(absorber_stdname))
        ds[var].attrs['units'] = UNITS.get(var, 'molec cm-3')

    return ds


def read_sce_aerosol(fn, altitude):
    """Read an ``SCE_AEROSOL.OUT`` file from SCIATRAN

    Parameters
    ----------
    fn : str
        Path to the output_map file

    altitude : xarray.DataArray
        The altitude grid of the SCIARTAN run.  This is needed to assign the
        aerosol parameters which are defined per SCIATRAN aerosol "layer" to
        the individual levels of the scenario.

    Returns
    -------
    sce_aerosol : xarray.Dataset
        All information contained in the ``SCE_AEROSOL.OUT`` file.

    Notes
    -----
    This function currently only works with the *manual* aerosol mode in
    SCIATRAN.

    """
    with open(fn, "r") as fd:
        lines = fd.readlines()

    # check for manual aerosol settings
    if len([l for l in lines if l.strip().lower().find('manual')]) == 0:
        raise NotImplementedError(
            'Reading SCE_AEROSOL.OUT is only supported for MANUAL '
            'aerosol settings')

    # find out wavelengths and AOT
    lines_wl = [l for l in lines if l.strip().startswith('Wavelength')]
    wavelength = [l.lower().split('wavelength')[1].split('[nm]')[0].strip()
                  for l in lines_wl]
    wavelength = [float(wl) for wl in wavelength]
    aot = [float(l.lower().strip().split('aot =')[1].split('[nm]')[0].strip())
           for l in lines_wl]

    # prepare for iteration over all lines, checking for profiles, expansion
    # coefficients, and asymmetry factors
    profiles = []
    asymmetry_factors = []
    expansion_coefficients = []
    curr_in_profile = False
    n_profile_start = -1
    for i, l in enumerate(lines):
        if l.strip() == '':
            if not curr_in_profile:
                continue
            # at this point, we're at the first blank line after profile ends.
            # here, we know the number of lines to read for getting the full
            # profile.  specifically, n_profile_start must have been set before
            assert n_profile_start > -1
            n_profile_end = i
            profile_curr = pd.read_csv(
                fn, delim_whitespace=True, skiprows=n_profile_start + 1,
                nrows=n_profile_end - n_profile_start - 1, header=None,
                names=['layer', 'altitude', 'extinction_coefficient',
                       'single_scattering_albedo'],
                index_col='layer')
            profiles.append(profile_curr)
            curr_in_profile = False
        # profiles start with +++++++++++++++++ line
        if l.strip().startswith('++++++++++++++++++++++++++'):
            if curr_in_profile:
                raise ValueError('Error parsing SCE_AEROSOL.OUT')
            curr_in_profile = True
            n_profile_start = i + 1
        # read asymmetry factors
        if l.strip().startswith('Asymmetry factor used in the aerosol layers'):
            asymmetry_factor_curr = pd.read_csv(
                fn, delim_whitespace=True, skiprows=i + 3, nrows=1,
                index_col='aerosol_layer', header=None,
                names=['aerosol_layer', 'altitude_top', 'altitude_bottom',
                       'asymmetry_factor'])
            asymmetry_factors.append(asymmetry_factor_curr)
        # read number of expansion coefficients
        if l.strip().startswith('Number of expansion coeff. and Delta-M fact'):
            expansion_coefficients_curr = pd.read_csv(
                fn, delim_whitespace=True, skiprows=i + 3, nrows=1,
                index_col='aerosol_layer', header=None,
                names=['aerosol_layer', 'altitude_top', 'altitude_bottom',
                       'n_exp_coeff', 'delta_m'])
            expansion_coefficients.append(expansion_coefficients_curr)

    # aggregate output
    aerosol_optical_thickness = xr.DataArray(
        aot, {'aerosol_wavelength': wavelength}, ['aerosol_wavelength'])

    # prepare output arrays
    n_exp_coeff = xr.DataArray(
        np.zeros((len(wavelength), altitude.size), dtype=int),
        {'layer': altitude['layer'], 'aerosol_wavelength': wavelength},
        ['aerosol_wavelength', 'layer'])
    delta_m = xr.DataArray(
        np.zeros((len(wavelength), altitude.size)),
        {'layer': altitude['layer'], 'aerosol_wavelength': wavelength},
        ['aerosol_wavelength', 'layer'])
    asymmetry_factor = delta_m.copy()
    extinction_coeff = delta_m.copy()
    ssa = delta_m.copy()

    # fill per-aerosol-layer information
    for ix_wl, (exp_coeff_, asymmetry_factor_) in enumerate(zip(
            expansion_coefficients, asymmetry_factors)):
        for lay in exp_coeff_.index:
            z_min, z_max = exp_coeff_.ix[lay][
                ['altitude_bottom', 'altitude_top']].values
            ix = (z_min <= altitude.values) & (altitude.values <= z_max)
            n_exp_coeff[ix_wl, ix] = exp_coeff_.ix[lay]['n_exp_coeff']
            delta_m[ix_wl, ix] = exp_coeff_.ix[lay]['delta_m']
            asymmetry_factor[ix_wl, ix] = asymmetry_factor_.ix[lay][
                'asymmetry_factor']

    # prepare extinction and ssa profiles
    for ix_wl, profile_ in enumerate(profiles):
        extc_tmp = extinction_coeff[ix_wl].copy()
        extc_tmp.loc[profile_.index] = profile_[
            'extinction_coefficient'].values
        extinction_coeff[ix_wl] = extc_tmp.copy()
        ssa[ix_wl].loc[profile_.index] = profile_['single_scattering_albedo']

    ds = xr.Dataset({'aerosol_optical_thickness': aerosol_optical_thickness,
                     'aerosol_asymmetry_factor': asymmetry_factor,
                     'aerosol_delta_m': delta_m,
                     'aerosol_n_exp_coeff': n_exp_coeff,
                     'aerosol_extinction_coeff': extinction_coeff,
                     'aerosol_single_scattering_albedo': ssa})

    # add metadata
    ds['aerosol_wavelength'].attrs['units'] = 'nm'
    ds['aerosol_wavelength'].attrs['standard_name'] = 'radiation_wavelength'
    ds['aerosol_wavelength'].attrs['comment'] = (
        'In SCIATRAN, aerosol characteristics are defined at these '
        'wavelengths.  SCIATRAN linearly interpolates from these '
        'wavelengths.  The corresponding variables are called "aerosol_*" '
        'in this file.')
    ds['aerosol_single_scattering_albedo'].attrs['standard_name'] = (
        'single_scattering_albedo_in_air_due_to_ambient_aerosol_particles')
    ds['aerosol_extinction_coeff'].attrs['standard_name'] = (
        'volume_extinction_coefficient_in_air_due_to_ambient_aerosol_'
        'particles')
    ds['aerosol_extinction_coeff'].attrs['units'] = 'km -1'
    ds['aerosol_optical_thickness'].attrs['standard_name'] = (
        'atmosphere_absorption_optical_thickness_due_to_ambient_aerosol_'
        'particles')
    ds['aerosol_n_exp_coeff'].attrs['units'] = '1'
    ds['aerosol_n_exp_coeff'].attrs['comment'] = (
        'The number of expansion coefficients used to describe the aerosol '
        'phase function.')
    # TODO ds['aerosol_delta_m'].attrs['comment'] = ''

    # TODO read phase function?

    return ds


def calc_layer_bounds(altitude):
    """Calculate lower and upper boundaries for SCIATRAN vertical layers

    Parameters
    ----------
    altitude : xarray.DataArray

    Returns
    -------
    altitude_bnds : xarray.DataArray

    """
    zmin = (((altitude.values[1:] + altitude.values[:-1]) / 2.).tolist() +
            [altitude.values[-1]])
    zmax = [1.5 * altitude.values[0] - 0.5 * altitude.values[1]] + zmin[:-1]
    zbnd = np.column_stack((zmin, zmax))
    altitude_bnds = xr.DataArray(zbnd, dict(layer=altitude['layer'],
                                            bnds=[0, 1]), ['layer', 'bnds'])
    return altitude_bnds


def _add_metadata_outputmap(ds):
    ds['sza'].attrs['units'] = 'degree'
    ds['sza'].attrs['standard_name'] = 'solar_zenith_angle'
    ds['sza'].attrs['long_name'] = 'solar zenith angle'
    ds['vza'].attrs['units'] = 'degree'
    ds['vza'].attrs['standard_name'] = 'viewing_zenith_angle'
    ds['vza'].attrs['long_name'] = 'viewing zenith angle'
    ds['raa'].attrs['units'] = 'degree'
    ds['raa'].attrs['standard_name'] = (
        'angle_of_rotation_from_solar_azimuth_to_platform_azimuth')
    ds['raa'].attrs['long_name'] = 'relative azimuth angle'
    ds['output_altitude'].attrs['units'] = 'km'
    ds['output_altitude'].attrs['long_name'] = 'output altitude'
    try:
        ds['stokes_component'].attrs['long_name'] = 'Stokes component'
        ds['stokes_component'].attrs['comment'] = (
            'number of the Stokes component')
    except (KeyError, IndexError):
        pass
    try:
        ds['tangent_height_geom'].attrs['units'] = 'km'
        ds['tangent_height_geom'].attrs['long_name'] = (
            'geometrical tangent height')
        ds['tangent_height_geom'].attrs['comment'] = (
            'geometrical tangent height in km (set to NaN if TH is not '
            'in the viewing direction)')
    except (KeyError, IndexError):
        pass
    try:
        ds['tangent_height_refr'].attrs['units'] = 'km'
        ds['tangent_height_refr'].attrs['long_name'] = (
            'refractive tangent height')
        ds['tangent_height_refr'].attrs['comment'] = (
            'refractive tangent height in km (set to NaN if TH is not in '
            'the viewing direction)')
    except (KeyError, IndexError):
        pass
    try:
        ds['sza_refr'].attrs['units'] = 'degree'
        ds['sza_refr'].attrs['long_name'] = 'refractive solar zenith angle'
        ds['sza_refr'].attrs['comment'] = (
            'solar zenith angle (refractive) at the tangent height or at '
            'the end of the line of sight(if TH is not in the viewing '
            'direction) in degrees (set to NaN if the point is not '
            'illuminated)')
    except (KeyError, IndexError):
        pass
    try:
        ds['ss_angle'].attrs['units'] = 'degree'
        ds['ss_angle'].attrs['long_name'] = 'single scattering angle'
        ds['ss_angle'].attrs['comment'] = (
            'single scattering angle (refractive) at the tangent height '
            'or at the end of the line for downward pointing LOS or at '
            'the first point for upward pointing LOS (set to NaN if the '
            'point is not illuminated')
    except (KeyError, IndexError):
        pass

    return ds


def read_output_map_legacy(fn):
    """Reads an ``output_map.inf`` file from SCIATRAN 3.0

    Parameters
    ----------
    fn : str
        Path to the output_map file

    Returns
    -------
    output_map : xarray.Dataset
        The output_map data

    """
    colnames_outputmap = [
        'sza', 'vza', 'raa', 'output_altitude']
    omap = pd.read_csv(
        fn, comment='#', index_col=0, delim_whitespace=True,
        names=colnames_outputmap)
    ds = xr.Dataset.from_dataframe(omap)
    ds.rename(dict(index='geometry'), inplace=True)

    # add metadata
    ds = _add_metadata_outputmap(ds)

    return ds


def read_output_map_36(fn):
    """Reads an ``output_map.inf`` file from SCIATRAN 3.6

    Parameters
    ----------
    fn : str
        Path to the output_map file

    Returns
    -------
    output_map : xarray.Dataset
        The output_map data

    """
    colnames_outputmap = [
        'geometry', 'stokes_component', 'sza', 'vza', 'raa', 'output_altitude']
    omap = pd.read_csv(
        fn, comment='#', index_col=0, delim_whitespace=True,
        names=colnames_outputmap)
    ds = xr.Dataset.from_dataframe(omap)

    # add metadata
    ds = _add_metadata_outputmap(ds)

    return ds


def read_output_map_38(fn):
    """Reads an ``output_map.inf`` file from SCIATRAN 3.8

    Parameters
    ----------
    fn : str
        Path to the output_map file

    Returns
    -------
    output_map : xarray.Dataset
        The output_map data

    """
    colnames_outputmap = [
        'geometry', 'stokes_component', 'sza', 'vza', 'raa',
        'tangent_height_geom', 'tangent_height_refr', 'sza_refr', 'ss_angle',
        'output_altitude']
    omap = pd.read_csv(
        fn, comment='#', index_col=0, delim_whitespace=True,
        names=colnames_outputmap,
        na_values={'tangent_height_geom': '999.00',
                   'tangent_height_refr': '999.00', 'sza_refr': '180.00',
                   'ss_angle': '90.00'})
    ds = xr.Dataset.from_dataframe(omap)

    # add metadata
    ds = _add_metadata_outputmap(ds)

    return ds


def read_n_spec_pts(fn):
    """Read number of spectral points from WF / BAMF output"""
    with open(fn, 'r') as fd:
        while True:
            l = fd.readline()
            tmp = l.split('The number of spectral points:')
            if len(tmp) > 1:
                return int(tmp[-1])
    raise ValueError('Number of spectral points not found in {}'.format(fn))


def read_n_altitude_lvls(fn):
    """Read number of altitude levels from WF / BAMF output"""
    with open(fn, 'r') as fd:
        while True:
            l = fd.readline()
            tmp = l.split('The number of altitude levels:')
            if len(tmp) > 1:
                return int(tmp[-1])
    raise ValueError('Number of altitude levels not found in {}'.format(fn))


def read_altitude(fn):
    """Read altitude grid from WF / BAMF output

    Parameters
    ----------
    fn : str
        Path to SCIATRAN output file to read

    """
    z = pd.read_csv(fn, comment='#', delim_whitespace=True, nrows=1,
                    header=None).values[0]
    if not np.all(z == np.sort(z)[::-1]):
        raise ValueError('Altitude grid from file {} seems to be junk'
                         ''.format(fn))
    return z


def read_wf_bamf(fn):
    """Read weighting function or block AMF from SCIATRAN output.

    Parameters
    ----------
    fn : str
        Path to SCIATRAN output file to read

    """
    try:
        raw = pd.read_csv(fn, delim_whitespace=True, header=None, skiprows=7,
                          dtype=np.float64).values
    except:
        raw = np.genfromtxt(fn, comments='#', skip_header=7)
        warnings.warn("WF/BAMF file {} couldn't be read with pd.read_csv.  "
                      "Falling back to np.genfromtxt".format(fn))
    n_spec = read_n_spec_pts(fn)
    n_z = read_n_altitude_lvls(fn)
    wl = raw[:n_spec, 0]
    da = xr.DataArray(
        np.zeros((raw.shape[1] - 1, n_z, n_spec)),
        {'wavelength': wl, 'layer': list(range(1, n_z + 1)),
         'geometry': list(range(1, raw.shape[1]))},
        ['geometry', 'layer', 'wavelength'])
    # the following is rather slow for weighting functions ...
    for i in range(n_spec):
        da[:, :, i] = raw[i::n_spec, 1:].T
    # TODO add name to DataArray
    return da


def read_irradiance(fn):
    """Read ``irradiance.dat`` from SCIATRAN output.

    Parameters
    ----------
    fn : str
        Path to SCIATRAN output file to read

    """
    raw = np.loadtxt(fn, comments="#")
    raw = np.atleast_2d(raw)
    wavelength = raw[:, 0]
    irrad = raw[:, 1]
    da = xr.DataArray(irrad, {'wavelength': wavelength}, ['wavelength'])
    da.name = 'irradiance'
    return da


def read_intensity(fn):
    """Read ``intensity.dat`` from SCIATRAN output.

    Parameters
    ----------
    fn : str
        Path to SCIATRAN output file to read

    """
    raw = np.loadtxt(fn, comments="#")
    raw = np.atleast_2d(raw)

    wavelengths = raw[:, 0]
    n_wl = wavelengths.size
    n_geom = raw.shape[1] - 1
    ix_geom = list(range(1, n_geom + 1))

    intens = raw[:, 1:].reshape((n_wl, n_geom)).T
    da = xr.DataArray(
        intens, {'wavelength': wavelengths, 'geometry': ix_geom},
        ['geometry', 'wavelength'])

    da.name = 'intensity'
    return da


def read_intensity_legacy(fn, stokes_vector=False):
    """Read ``intensity.dat`` from SCIATRAN output.

    Parameters
    ----------
    fn : str
        Path to SCIATRAN output file to read

    stokes_vector : bool
        If *True*, returns the full stokes vector of the intensity; if *False*,
        only the *I* component.

    """
    # check if scalar RT or vector RT
    mode = _get_rt_mode(fn)

    raw = np.loadtxt(fn, comments="#")
    raw = np.atleast_2d(raw)

    wavelengths = raw[:, 0]
    n_wl = wavelengths.size
    n_geom = raw.shape[1] - 1
    ix_geom = list(range(1, n_geom + 1))

    if mode in ["DOM-S", "CDI"]:
        intens = raw[:, 1:].reshape((n_wl, n_geom)).T
        da = xr.DataArray(
            intens, {'wavelength': wavelengths, 'geometry': ix_geom},
            ['geometry', 'wavelength'])

    elif mode == "DOM-V":
        intens = np.empty((n_geom, n_wl, 4))
        intens[:, :, 0] = raw[:, 1::4].reshape((n_wl, n_geom)).T
        intens[:, :, 1] = raw[:, 2::4].reshape((n_wl, n_geom)).T
        intens[:, :, 2] = raw[:, 3::4].reshape((n_wl, n_geom)).T
        intens[:, :, 3] = raw[:, 4::4].reshape((n_wl, n_geom)).T

        da = xr.DataArray(
            intens, {'wavelength': wavelengths, 'geometry': ix_geom,
                     'stokes_component': ['I', 'Q', 'U', 'V']},
            ['geometry', 'wavelength', 'stokes_component'])

        if not stokes_vector:
            da = da.loc['I']

    da.name = 'intensity'
    return da


def read_slant_col(fn):
    """Read ``slant_col.dat`` from SCIATRAN output.

    This function reads the full ``slant_col.dat`` file from SCIATRAN output
    and returns it as an xarray.DataArray.

    """
    raw = pd.read_csv(fn, comment='#', delim_whitespace=True,
                      header=None).values
    wavelengths = raw[:, 0]
    n_wl = wavelengths.size
    n_geom = raw.shape[1] - 1
    ix_geom = list(range(1, n_geom + 1))

    scd = raw[:, 1:].reshape((n_wl, n_geom)).T
    da = xr.DataArray(
        scd, {'wavelength': wavelengths, 'geometry': ix_geom},
        ['geometry', 'wavelength'])

    da.name = 'slant_col_{}'.format(_get_absorber_name_from_header(fn))
    return da


def read_vert_col(fn):
    """Read ``vert_col.dat`` from SCIATRAN output.

    This function reads the full ``vert_col.dat`` file from SCIATRAN output and
    returns it as an xarray.Dataset.

    """
    vcd = pd.read_csv(fn, comment='#', delim_whitespace=True,
                      names=['sza', 'vcd'])
    vcd = xr.Dataset.from_dataframe(vcd)
    vcd = vcd.rename(dict(
        index='geometry',
        vcd='vert_col_{}'.format(_get_absorber_name_from_header(fn))))
    vcd['geometry'] = list(range(1, vcd['geometry'].size + 1))
    return vcd


def detect_sciatran_version(fn, string=False):
    """Detect SCIATRAN version from output files

    This function parses the header of a ``*.dat`` or ``*.inf`` file to extract
    the SCIARTAN version.

    Parameters
    ----------
    fn : str
        Path to the SCIATRAN output file

    string : bool, optional
        If *True*, this function returns the version string.  If *False*, this
        function returns an instance of ``distutils.version.LooseVersion``.

    Returns
    -------
    version

    """
    with open(fn, 'r') as fd:
        while True:
            line = fd.readline()
            items = line.split()
            try:
                ix_version = items.index('SCIATRAN') + 1
            except ValueError:
                continue
            assert ix_version > 0
            version = items[ix_version]
            if string:
                return version
            return LooseVersion(version)


def add_array_to_output(output, arr, name):
    """Add a new array to the existing output Dataset.

    This function is necessary because sometimes, the wavelenths don't match
    exactly, and in those cases the xarray.Dataset.__setattr__ doesn't work
    properly, leading to NaN values in the resulting Dataset.

    """
    try:
        # First we check if the wavelength axes are identical.  If they are, we
        # can simply call output.update(arr) and everything will go fine
        xr.testing.assert_equal(output['wavelength'], arr['wavelength'])
    except AssertionError:
        # The wavelength axes are not identical
        try:
            # Now we check if the wavelength axes are almost identical.  If
            # they are, we assign the output's wavelength axis to the array, so
            # that we can later call output.update(arr).
            xr.testing.assert_allclose(arr['wavelength'], output['wavelength'])
            arr['wavelength'] = output['wavelength']
        except AssertionError:
            if 'wavelength' in output.data_vars:
                # Apparently, the wavelength axes aren't even remotely
                # identical.  Abort.
                raise
            else:
                # This seems to be the first time we add an array with
                # wavelength dimension to this output Dataset, so we just
                # proceed
                raise
                pass
    except KeyError:
        pass
    output.update(xr.Dataset({name: arr}), inplace=True)


def extract_results_archive(filename):
    """Extract SCIATRAN output archive to a temporary location

    Parameters
    ----------
    filename : str
        The archive containing the SCIATRAN output.

    Returns
    -------
    path : str
        The path of the temporary directory to which the archive is extracted.

    """
    if filename.lower().endswith('.zip'):
        with zipfile.ZipFile(filename, 'r') as fd:
            files = [p for p in fd.namelist() if p.startswith('DATA_OUT/')]
            if len(files) == 0:
                raise ValueError(
                    "The archive {} doesn't contain a DATA_OUT directory."
                    "".format(filename))
            path = tempfile.mkdtemp()
            fd.extractall(path, files)
    elif filename.lower().endswith('.tar'):
        with tarfile.open(filename, 'r:') as fd:
            files = [p for p in fd.getmembers()
                     if p.name.startswith('DATA_OUT/')]
            if len(files) == 0:
                raise ValueError(
                    "The archive {} doesn't contain a DATA_OUT directory."
                    "".format(filename))
            path = tempfile.mkdtemp()
            fd.extractall(path, files)
    elif filename.lower().endswith('.tar.gz'):
        with tarfile.open(filename, 'r:gz') as fd:
            files = [p for p in fd.getmembers()
                     if p.name.startswith('DATA_OUT/')]
            if len(files) == 0:
                raise ValueError(
                    "The archive {} doesn't contain a DATA_OUT directory."
                    "".format(filename))
            path = tempfile.mkdtemp()
            fd.extractall(path, files)
    elif filename.lower().endswith('.tar.bz2'):
        with tarfile.open(filename, 'r:bz2') as fd:
            files = [p for p in fd.getmembers()
                     if p.name.startswith('DATA_OUT/')]
            if len(files) == 0:
                raise ValueError(
                    "The archive {} doesn't contain a DATA_OUT directory."
                    "".format(filename))
            path = tempfile.mkdtemp()
            fd.extractall(path, files)
    elif filename.lower().endswith('.tar.xz'):
        with tarfile.open(filename, 'r:xz') as fd:
            files = [p for p in fd.getmembers()
                     if p.name.startswith('DATA_OUT/')]
            if len(files) == 0:
                raise ValueError(
                    "The archive {} doesn't contain a DATA_OUT directory."
                    "".format(filename))
            path = tempfile.mkdtemp()
            fd.extractall(path, files)
    else:
        raise ValueError('Cannot extract SCIATRAN output from {}'
                         ''.format(filename))

    path = os.path.join(path, 'DATA_OUT')
    return path


def reshape_stokes_array(ds):
    """Reshape all vectorized RT variable arrays

    By default, pyatran organizes SCIATRAN output according to
    ``output_map.inf``.  In recent SCIATRAN versions, this includes information
    on the Stokes vector.  Effectively, this means that the Stokes component is
    treated as part of the simulation geometry.

    This function reshapes all relevant variables (*intensity*,
    *intensity_noring*, *ring*) to contain an additional third dimension
    *stokes_component*.

    Parameters
    ----------
    ds : xarray.Dataset
        The SCIATRAN output Dataset to be reshaped

    output_map : xarray.Dataset

    Returns
    -------
    ds_new : xarray.Dataset

    """
    STOKES_VECTOR = ['I', 'Q', 'U', 'V']

    VARS_OUTPUT_MAP = [
        'sza', 'vza', 'raa', 'tangent_height_geom', 'tangent_height_refr',
        'sza_refr', 'ss_angle', 'output_altitude']

    VARS_VECTORIZED = ['intensity', 'intensity_noring', 'ring']
    vector_variables = [v for v in ds.data_vars if v in VARS_VECTORIZED]

    WARNING_TEXT_NO_VEC = (
        "`reshape_stokes_array` couldn't find any vectorized quantity in data")

    if 'stokes_component' not in ds.data_vars:
        raise NotImplementedError(
            "`reshape_stokes_array` is only implemented for recent SCIATRAN "
            "versions.  If you need this functionality for old SCIATRAN "
            "output, please contact the pyatran developers.")

    elif not vector_variables:
        # ds doesn't contain any output where we expect stokes_component dim
        return ds

    elif not ((ds['stokes_component'] != 1).any() and
              (ds['stokes_component'] != 'I').any()):

        # ds does contain output where we expect stokes_component dim, but
        # there is only one stokes_component in output_map.
        # FIXME figure out from SCE_INP-PARS if we really expect vector output
        warnings.warn(WARNING_TEXT_NO_VEC)
        return ds

    # rename the original geometry axis
    ds.rename({'geometry': 'geometry_old'}, inplace=True)

    # gather information on stokes component
    n_stokes = np.unique(ds['stokes_component'].values).size
    stokes_outputmap = ds['stokes_component'].copy()
    stokes_list_new = stokes_outputmap.values[:n_stokes].tolist()
    del ds['stokes_component']

    # reshape data arrays
    for var in VARS_VECTORIZED:
        if var in ds.data_vars:
            arr = ds[var]
            n_geom = arr.shape[0] // n_stokes
            n_wl = arr.shape[1]

            arr_new = xr.DataArray(
                np.zeros((n_geom, n_stokes, n_wl)),
                {'geometry': range(1, n_geom + 1),
                 'stokes_component': STOKES_VECTOR[:n_stokes],
                 'wavelength': arr['wavelength']},
                ['geometry', 'stokes_component', 'wavelength'])

            for i, v in enumerate(stokes_list_new):
                if stokes_outputmap is not None:
                    ix = (stokes_outputmap == v)
                else:
                    ix = np.arange(1, arr.shape[0] + 1) % n_stokes == i
                arr_new[:, i, :] = arr[ix, :]

            ds[var] = arr_new
            no_var = False

    # test if outputmap can be compressed
    ixs = []
    for i in stokes_list_new:
        ixs.append(stokes_outputmap == stokes_outputmap[i])
    for j in ixs[1:]:
        for var in VARS_OUTPUT_MAP:
            np.testing.assert_equal(
                ds[var][ixs[0]].values, ds[var][j].values,
                "Cannot collapse output_map data.")

    # adapt output_map
    ix = np.arange(arr.shape[0]) % n_stokes == 0
    for var in VARS_OUTPUT_MAP:
        ds[var] = xr.DataArray(
            ds[var][ix].values, {'geometry': range(1, n_geom + 1)},
            ['geometry'])
    del ds._dims['geometry_old'], ds['geometry_old']

    if no_var:
        warnings.warn(WARNING_TEXT_NO_VEC)

    return ds


def fix_output_map_domv_bug_38(output_map, ds):
    """Fix output_map information

    There is a bug in SCIATRAN < 3.8.6 which leads to wrong output_map
    information in case of DOM_V simulations in ``raman`` mode.

    Parameters
    ----------
    output_map : xarray.Dataset

    ds : xarray.Dataset

    Returns
    -------
    output_map_new : xarray.Dataset

    """
    VARS_OUTPUT_MAP = [
        'sza', 'vza', 'raa', 'tangent_height_geom', 'tangent_height_refr',
        'sza_refr', 'ss_angle', 'output_altitude']
    VARS_DOMVOUTPUTMAP_BUG = [
        'block_amf', 'slant_col', 'amf', 'intensity_noring']

    # read the shape of the data variables
    vars = [v for v in ds.data_vars if v in VARS_DOMVOUTPUTMAP_BUG]
    n_geom_arr = ds[vars[0]].shape[0]
    n_geom_opm = output_map['sza'].size

    if n_geom_arr == n_geom_opm:
        # apparently this output data is not affected by the bug.  maybe only
        # the 'I' component was writte to output?  Or, other possibility, this
        # is output for a quantity which is scalar, like amf, slant_col,
        # block_amf.
        return output_map

    guess_n_stokes_list = [(n_geom_opm * i == n_geom_arr) for i in range(1, 5)]
    assert sum(guess_n_stokes_list) == 1, "Cannot guess Stokes components"
    n_stokes = guess_n_stokes_list.index(True) + 1

    output_map_new = xr.Dataset()

    for var in VARS_OUTPUT_MAP:
        v_new = xr.DataArray(
            np.zeros(n_geom_arr),
            {'geometry': np.arange(1, n_geom_arr + 1)},
            ['geometry'])
        for i in range(n_geom_opm):
            v_new[i * n_stokes:(i + 1) * n_stokes] = output_map[var][i].values
        output_map_new[var] = v_new

    sc_new = xr.DataArray(
        np.tile(np.arange(1, n_stokes + 1), n_geom_opm),
        {'geometry': np.arange(1, n_geom_arr + 1)},
        ['geometry'])
    sc_new.attrs['comments'] = (
        "Due to a bug in SCIARTAN versions < 3.8.6, the original SCIATRAN "
        "output didn't contain information on the Stokes component.  This "
        "array therefore only contains a plausible guess.")
    sc_new.attrs['long_name'] = 'Stokes component'
    output_map_new['stokes_component'] = sc_new

    return output_map_new


def _add_str_to_comment(ds, var, s):
    """Add a string to the `comment` attribute of an array in a Dataset"""
    c_ = ds[var].attrs.get('comment')
    c_ = '' if c_ is None else str(c_)
    if c_.endswith('.'):
        c_ += '  '
    ds[var].attrs['comment'] = c_ + s
    return ds


def read_sciatran_output(path, absorbers='all', stokes_dim=True):
    """Read SCIATRAN output

    Parameters
    ----------
    path : str
        Path to SCIATRAN output.

    absorbers : list of str
        Read relevant output only for these absorbers.  If ``all``, all
        absorbers' output will be read, which can be slow.

    stokes_dim : bool
        If *True*, output arrays of vectorized radiative transfer (i.e.,
        *DOM_V*) simulations will have an additional dimension
        ``stokes_component``.  If *False*, the Stokes component will be encoded
        as part of the ``geometry`` dimension (as a direct replication of
        SCIATRAN's ``output_map.inf`` file).

        In case of scalar radiative transfer (i.e., *DOM_S* or *CDI*), the
        output will not contain the Stokes component as dimension, irrespective
        of this setting.

    Returns
    -------
    output : xarray.Dataset
        The full SCIATRAN output in one single data structure

    """
    # will be set later in case of archived results
    delete_path = False

    # extract results archive, if necessary
    if os.path.isdir(path):
        p_do = path
    else:
        p_do = extract_results_archive(path)
        delete_path = True

    # prepare list of absorbers to read, all in lower case
    if absorbers != 'all':
        if isinstance(absorbers, str):
            absorbers = [absorbers.lower()]
        else:
            absorbers = [k.lower() for k in absorbers]
    else:
        absorbers = []

    try:
        version = detect_sciatran_version(os.path.join(p_do,
                                                       'SCE_INP-PARS.OUT'))
    except (FileNotFoundError, OSError):
        raise ValueError('Cannot read SCIATRAN version information')

    # create empty output Dataset
    output = xr.Dataset()

    # read output map.  this is the only file we can be sure exists
    if version < LooseVersion('3.5'):
        output_map = read_output_map_legacy(
            os.path.join(p_do, 'output_map.inf'))
    elif LooseVersion('3.6') <= version < LooseVersion('3.8'):
        output_map = read_output_map_36(os.path.join(p_do, 'output_map.inf'))
    else:
        output_map = read_output_map_38(os.path.join(p_do, 'output_map.inf'))

    # read absorber profiles
    sce_absorber = read_sce_absorber(os.path.join(p_do, 'SCE_ABSORBER.OUT'))
    output.update(sce_absorber)

    # calculate altitude bounds
    altitude_bnds = calc_layer_bounds(output['altitude'])
    output.update(xr.Dataset({'altitude_bnds': altitude_bnds}), inplace=True)
    output['altitude'].attrs['bounds'] = 'altitude_bnds'

    # read aerosol information
    try:
        sce_aerosol = read_sce_aerosol(os.path.join(p_do, 'SCE_AEROSOL.OUT'),
                                       output['altitude'])
        output.update(sce_aerosol)
    except (FileNotFoundError, OSError):
        pass

    # read intensity
    try:
        intens = read_intensity(os.path.join(p_do, 'intensity.dat'))
        add_array_to_output(output, intens, 'intensity')
    except (FileNotFoundError, OSError):
        pass

    # read intensity_noring
    try:
        intens_noring = read_intensity(
            os.path.join(p_do, 'intensity_noring.dat'))
        add_array_to_output(output, intens_noring, 'intensity_noring')
    except (FileNotFoundError, OSError):
        pass

    # read irradiance
    try:
        irrad = read_irradiance(os.path.join(p_do, 'irradiance.dat'))
        add_array_to_output(output, irrad, 'irradiance')
    except (FileNotFoundError, OSError):
        pass

    # read weighting functions
    fns_wf = glob(os.path.join(p_do, 'wf_*.dat'))
    for fn in fns_wf:
        key = os.path.splitext(os.path.split(fn)[1])[0]
        if key.split('_')[1] in absorbers or not absorbers:
            add_array_to_output(output, read_wf_bamf(fn), key)

    # read slant columns
    try:
        scd = read_slant_col(os.path.join(p_do, 'slant_col.dat'))
        add_array_to_output(output, scd, scd.name)
    except (FileNotFoundError, OSError):
        pass

    # read vertical columns
    try:
        vcd = read_vert_col(os.path.join(p_do, 'vert_col.dat'))
        # read_vert_col returns a Dataset, but we are only interested in the
        # vcd value.  So we delete the sza variable and then pass only the vcd
        # array to add_array_to_output
        del vcd['sza']
        vcd_name_ = [v for v in vcd.data_vars][0]
        add_array_to_output(output, vcd[vcd_name_], vcd_name_)
    except (FileNotFoundError, OSError):
        pass

    # read block amf
    try:
        bamf = read_wf_bamf(os.path.join(p_do, 'block_amf.dat'))
        add_array_to_output(output, bamf, 'block_amf')
    except (FileNotFoundError, OSError):
        pass

    # add version information
    output.attrs['SCIATRAN_version'] = str(version)
    output.attrs['pyatran_version'] = pyatran.__version__

    # find out if we're doing DOM_V
    dom_v = read_inp_par(
        os.path.join(p_do, 'SCE_INP-PARS.OUT'), 'RTM-CORE') == 'DOM_V'

    # in SCIATRAN < 3.8.6 there's a bug in output_map.inf for some DOM_V cases
    # FIXME add lower bound on version number -- this bug appeared sometime
    if (dom_v and (version < LooseVersion('3.8.6')) and
            [v for v in output.data_vars
             if v in ['slant_col', 'amf', 'block_amf', 'intensity_noring']]):
        output_map = fix_output_map_domv_bug_38(output_map, output)

    output.update(output_map)

    if stokes_dim and dom_v:
        output = reshape_stokes_array(output)

    # add comments / warnings to some variables, depending on SCIATRAN bugs
    WARNING_BAMF_ALTZ = (
        "This altitutde grid represents the standard RT altitude grid from "
        "SCIATRAN, not the post-processed `z_bamf` altitude grid.")
    if 'block_amf' in output.data_vars and (version >= LooseVersion('3.8.3')):
        output = _add_str_to_comment(output, 'altitude', WARNING_BAMF_ALTZ)

    WARNING_SZA_GEOM = (
        "This version of SCIARTAN was affected by a bug leading to wrong SZAs "
        "being written to the output files.  This variable `sza` therefore "
        "contains the *refractive* solar zenith angles instead of the "
        "*geometrical* ones."
    )
    if ((LooseVersion('3.8.0') <= version <= LooseVersion('3.8.5')) and
            (output['sza'].values == output['sza_refr'].values).all()):
        output = _add_str_to_comment(output, 'sza', WARNING_SZA_GEOM)

    WARNING_BAMF_ALT_BNDS = (
        "These altitude bounds are an approximation of the altitude grid used "
        "internally by SCIATRAN.  Due to the internal workings of the "
        "`block_amf` mode in SCIATRAN, these altitude bounds might not be "
        "suited for calculating column air mass factors.  This discussion is "
        "ongoing; please use these data at your own risk.")
    if 'block_amf' in output.data_vars:
        output = _add_str_to_comment(
            output, 'altitude_bnds', WARNING_BAMF_ALT_BNDS)

    # delete temporary directory, if necessary
    if delete_path and p_do:
        assert p_do != path
        if os.path.split(p_do)[1] == 'DATA_OUT':
            p_do = os.path.split(p_do)[0]
        assert p_do != path
        shutil.rmtree(p_do)

    return output
