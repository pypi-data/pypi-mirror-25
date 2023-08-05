# -*- coding: utf-8 -*-
from __future__ import unicode_literals, with_statement, division

import glob
import os
import shutil
import tempfile
import warnings
import zipfile

import numpy as np
from numpy.testing import assert_array_equal
import pandas as pd


class Result(dict):
    """Reading SCIATRAN's ``DATA_OUT`` directory.

    The *Result* class reads output from SCIATRAN's ``DATA_OUT``
    directory and stores the results in pandas data structures.

    Parameters
    ----------
    path : str
        Path to the ``DATA_OUT`` directory of the SCIATRAN run.  This
        can be either an actual filesystem path to the ``DATA_OUT``
        directory, or it can be the filename of a ``.zip`` file
        containing the ``DATA_OUT`` (i.e., there has to be a folder
        ``DATA_OUT`` at the root of the ``.zip`` file) directory.

    Notes
    -----
    Creating an instance of the ``Result`` class automatically reads
    all available information from *path*; i.e., no explicit calling
    of the ``read_*`` methods is necessary.

    Currently, only the following SCIATRAN output files can be read:

    - ``SCE_ABSORBER.OUT``
    - ``SCE_SUMMARY.OUT``
    - ``aer_abs.dat``
    - ``aer_sca.dat``
    - ``amf.dat``
    - ``bamf_int.dat``
    - ``block_amf.dat``
    - ``cld_abs.dat``
    - ``cld_sca.dat``
    - ``gas_abs.dat``
    - ``height.dat``
    - ``intensity.dat``
    - ``intensity_noring.dat``
    - ``irradiance.dat``
    - ``output_map.inf``
    - ``profiles_nd.dat``
    - ``profiles_vmr.dat``
    - ``ray_sca.dat``
    - ``ring.dat``
    - ``slant_col.dat``
    - ``tg_vod.dat``
    - ``vod_all.dat``
    - ``wf_*.dat``

    """
    __setattr__ = dict.__setitem__

    __delattr__ = dict.__delitem__

    def __getattr__(self, attr):
        return self.get(attr)

    def __dir__(self):
        return self.keys()

    def __init__(self, path):
        warnings.warn('The Result class is deprecated in favor of the new '
                      'read_sciatran_output mechanism.', DeprecationWarning)
        self._tmpdir = False
        if os.path.isdir(path):
            self.path = path
        elif os.path.splitext(path)[1].lower() == ".zip":
            try:
                with zipfile.ZipFile(path, "r") as fd:
                    self.path = tempfile.mkdtemp()
                    files = [p for p in fd.namelist()
                             if p.startswith("DATA_OUT")]
                    fd.extractall(self.path, files)
            except IOError:
                raise
            self.path = os.path.join(self.path, "DATA_OUT")
            self._tmpdir = True
        else:
            raise ValueError("I don't understand the value you passed for "
                             "'path', which was '{}'".format(path))
        self.path = os.path.normpath(self.path)

        self.output_map = self.read_output_map()
        self.SCE_ABSORBER = self.read_SCE_ABSORBER()
        self.SCE_SUMMARY = self.read_SCE_SUMMARY()

        # try to read intensity
        try:
            self.intensity = self.read_intensity("intensity.dat")
        except IOError as err:
            if err.errno != 2:  # failure *not* due to missing file
                raise

        # try to read intensity_noring
        try:
            self.intensity_noring = self.read_intensity("intensity_noring.dat")
        except IOError as err:
            if err.errno != 2:  # failure *not* due to missing file
                raise

        # try to read ring
        try:
            self.ring = self.read_intensity("ring.dat")
        except IOError as err:
            if err.errno != 2:  # failure *not* due to missing file
                raise

        # try to read irradiance
        try:
            self.irradiance = self.read_irradiance()
        except IOError as err:
            if err.errno != 2:  # failure *not* due to missing file
                raise

        # try to read slant column
        try:
            self.slant_col = self.read_slant_col()
        except IOError as err:
            if err.errno is not None:
                if err.errno != 2:  # failure *not* due to missing file
                    raise
            elif hasattr(err, "message"):
                if not (err.message.startswith("File ") and
                        err.message.endswith(" does not exist")):
                    raise

        # try to read air mass factor
        try:
            self.amf = self.read_amf(filename="amf.dat")
        except IOError as err:
            if err.errno is not None:
                if err.errno != 2:  # failure *not* due to missing file
                    raise
            elif err.message:
                if not (err.message.startswith("File ") and
                        err.message.endswith(" does not exist")):
                    raise

        # try to read block air mass factor
        try:
            self.block_amf = self.read_block_amf()
        except IOError as err:
            if err.errno != 2:  # failure *not* due to missing file
                raise
        try:
            self.bamf_int = self.read_amf(filename="bamf_int.dat")
        except IOError as err:
            if err.errno != 2:  # failure *not* due to missing file
                raise

        # try to read vertical optical depth
        try:
            self.tg_vod = self.read_tg_vod()
        except IOError as err:
            if err.errno != 2:  # failure *not* due to missing file
                raise
        try:
            self.vod_all = self.read_vod_all()
        except IOError as err:
            if err.errno != 2:  # failure *not* due to missing file
                raise

        # try to read weighting functions
        files_wf = glob.glob(os.path.join(self.path, "wf_*.dat"))
        for fn in files_wf:
            species = os.path.splitext(os.path.split(fn)[1])[0].split("_")[1]
            try:
                setattr(self, "wf_{}".format(species), self.read_wf(fn))
            except IOError as err:
                if err.errno != 2:  # failure *not* due to missing file
                    raise

        # try to read retrieved profiles
        try:
            self.profiles_vmr = self.read_profiles("vmr")
        except IOError as err:
            if err.errno != 2:  # failure *not* due to missing file
                raise
        try:
            self.profiles_conc = self.read_profiles("conc")
        except IOError as err:
            if err.errno != 2:  # failure *not* due to missing file
                raise

        # try to read vertical profiles of optical properties
        # controlled by "Write local optical parameters" in control_out.inp
        try:
            self.local_optical_params = self.read_local_optical_parameters()
        except IOError as err:
            pass

    def __del__(self):
        if self._tmpdir:
            shutil.rmtree(os.path.split(self.path)[0])

    def _get_rt_mode_from_output(self, fn):
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

    def read_output_map(self):

        def _assert_domv_geometries(output_map):
            # With vector RT, the output_map contains one line per Stokes
            # parameter, with identical geometries.  This method asserts
            # that the lines for all four Stokes parameters are actually
            # identical.
            o_ = output_map.copy()
            try:
                del o_["stokes_component"]
                _colname = 'stokes_component'
            except KeyError:
                del o_["SC"]
                _colname = 'SC'
            for i in [2, 3, 4]:
                assert_array_equal(np.asarray(o_[output_map[_colname] == 1]),
                                   np.asarray(o_[output_map[_colname] == i]))

        fn = os.path.join(self.path, "output_map.inf")

        # get last header line of output_map.inf
        with open(fn, "r") as fd:
            for line in fd:
                if line.startswith("#"):
                    last_header_ = line

        # determine column names
        last_header_ = last_header_[1:].strip()
        raw_cols_ = last_header_.replace(";", ",").split(",")
        raw_cols_ = [r.strip() for r in raw_cols_]

        colname_dict_ = {"Number": "Number",
                         "Num.": "Number",
                         "SZA": "sza",
                         "solar zenith angle": "sza",
                         "LOS angle": "los",
                         "azimuth angle(@ TOA)": "azim",
                         "azimuth angle(@ Observer position)": "azim",
                         "output altitude": "out_altitude",
                         "trace gas label": "trace_gas",
                         "SC": "stokes_component"}

        cols_ = [colname_dict_[key] for key in raw_cols_]

        output_map = pd.read_csv(fn, comment="#", header=None, names=cols_,
                                 skipinitialspace=True, sep=r"\s+",
                                 engine="python")
        output_map = output_map.dropna(how='all')
        output_map.index = output_map["Number"].astype(int)
        output_map.index.name = "Geometry"
        del output_map["Number"]

        # verify if stokes component column makes sense
        if "stokes_component" in output_map.columns:
            if output_map["stokes_component"].unique().size == 1:
                try:
                    mode = self._get_rt_mode_from_output(fn)
                    if mode == "DOM-V":
                        warnings.warn("'output_map.inf' indicates vector RT, "
                                      "but doesn't contain information on the "
                                      "Stokes components.")
                except Exception:
                    pass

            elif output_map["stokes_component"].unique().size == 4:
                mode = self._get_rt_mode_from_output(fn)

                if mode in ["DOM-S", "CDI"]:
                    raise ValueError("'output_map.inf' indicates scalar RT, "
                                     "but does contain information on the "
                                     "Stokes components.")
                try:
                    _assert_domv_geometries(output_map)
                except AssertionError:
                    raise ValueError("'output_map.inf' contains information "
                                     "on Stokes components, but the "
                                     "geometries for the individual Stokes "
                                     "components don't match!")
                # select unique geometries
                try:
                    output_map = output_map[
                        output_map['stokes_component'] == 1]
                except KeyError:
                    output_map = output_map[output_map['SC'] == 1]

                # reindex dataframe
                output_map.index = np.arange(1, output_map.shape[0] + 1,
                                             dtype=int)
            else:
                raise ValueError("I don't understand the contents of the 'SC' "
                                 "column of 'output_map.inf'")

        return output_map

    def read_intensity(self, filename="intensity.dat"):
        fn = os.path.join(self.path, filename)

        # check if scalar RT or vector RT
        mode = self._get_rt_mode_from_output(fn)

        n_geom = self.output_map.shape[0]

        raw = np.loadtxt(fn, comments="#")
        raw = np.atleast_2d(raw)

        wavelengths = raw[:, 0]
        n_wl = wavelengths.size

        if mode in ["DOM-S", "CDI"]:
            intens = raw[:, 1:].reshape((n_wl, n_geom)).T
            df = pd.DataFrame(intens, columns=wavelengths,
                              index=self.output_map.index)
            df.index.name = "Geometry"
            df.columns.name = "Wavelength"

        elif mode == "DOM-V":
            intens_I = raw[:, 1::4].reshape((n_wl, n_geom)).T
            intens_Q = raw[:, 2::4].reshape((n_wl, n_geom)).T
            intens_U = raw[:, 3::4].reshape((n_wl, n_geom)).T
            intens_V = raw[:, 4::4].reshape((n_wl, n_geom)).T

            df = pd.Panel(dict(I=pd.DataFrame(intens_I, columns=wavelengths,
                                              index=self.output_map.index),
                               Q=pd.DataFrame(intens_Q, columns=wavelengths,
                                              index=self.output_map.index),
                               U=pd.DataFrame(intens_U, columns=wavelengths,
                                              index=self.output_map.index),
                               V=pd.DataFrame(intens_V, columns=wavelengths,
                                              index=self.output_map.index)))
            df.items.name = "Stokes component"
            df.major_axis.name = "Geometry"
            df.minor_axis.name = "Wavelength"

        return df

    def read_irradiance(self):
        fn = os.path.join(self.path, "irradiance.dat")

        raw = np.loadtxt(fn, comments="#")
        raw = np.atleast_2d(raw)

        wavelengths = raw[:, 0]
        irrad = raw[:, 1]
        df = pd.Series(irrad, index=wavelengths)
        df.index.name = "Wavelength"

        return df

    def read_amf(self, filename):
        fn = os.path.join(self.path, filename)

        amf = pd.read_csv(fn, comment="#", header=None, skipinitialspace=True,
                          sep=r"\s+", index_col=0, engine="python").T
        amf.index.name = self.output_map.index.name
        amf.columns.name = "Wavelength"

        return amf

    def read_slant_col(self):
        fn = os.path.join(self.path, "slant_col.dat")

        scd = pd.read_csv(fn, comment="#", header=None, skipinitialspace=True,
                          sep=r"\s+", index_col=0, engine="python").T
        scd.index.name = self.output_map.index.name
        scd.columns.name = "Wavelength"
        return scd

    def read_block_amf(self):
        fn = os.path.join(self.path, "block_amf.dat")

        with open(fn, "r") as fd:
            for l in fd.readlines():
                if l.startswith("#"):
                    continue
                altitude = np.asarray(l.split(), dtype=float)
                break

        n_geom = self.output_map.shape[0]
        n_alt = altitude.shape[0]

        raw = np.loadtxt(fn, skiprows=6, comments="#")

        wavelengths = raw[:raw.shape[0] / n_alt, 0]
        n_wl = wavelengths.shape[0]

        bamf = raw[:, 1:].reshape((n_alt, n_wl, n_geom))

        df = pd.Panel(bamf, items=altitude, major_axis=wavelengths,
                      minor_axis=self.output_map.index)
        df.items.name = "Altitude"
        df.major_axis.name = "Wavelength"
        df.minor_axis.name = "Geometry"

        return df

    def read_profiles(self, qty):
        if qty == "vmr":
            fn = os.path.join(self.path, "profiles_vmr.dat")
        elif qty == "conc":
            fn = os.path.join(self.path, "profiles_nd.dat")
        else:
            raise ValueError("I don't understand what you mean by passing the "
                             "value '{}' for 'qty'".format(qty))

        with open(fn, "r") as fd:
            header = fd.readlines()[:4]
        gases = header[1].split()
        # vcds = [float(s) for s in header[3].split()]
        raw = np.loadtxt(fn, skiprows=4)
        data = pd.Panel(items=["apriori", "last", "retrieved"],
                        major_axis=gases, minor_axis=raw[:, 0])
        for i, gas in enumerate(gases):
            data.ix["apriori", gas] = raw[:, i * 3 + 1]
            data.ix["last", gas] = raw[:, i * 3 + 2]
            data.ix["retrieved", gas] = raw[:, i * 3 + 3]
        del raw
        return data

    def read_vod_all(self):
        fn = os.path.join(self.path, "vod_all.dat")

        raw = np.loadtxt(fn, comments="#")
        raw = np.atleast_2d(raw)

        wavelengths = raw[:, 0]

        vod = raw[:, 1:]

        if vod.shape[1] == 5:
            columns = ["ray", "aer_scat", "aer_abs", "cld_scat", "tot"]
        elif vod.shape[1] == 6:
            columns = ["ray", "aer_scat", "aer_abs", "cld_scat", "cld_abs",
                       "tot"]

        df = pd.DataFrame(vod, index=wavelengths,
                          columns=columns)
        df.columns.name = "vod"
        df.index.name = "Wavelength"

        return df

    def read_tg_vod(self):
        fn = os.path.join(self.path, "tg_vod.dat")

        n_tg = self.output_map.shape[0]

        raw = np.loadtxt(fn, comments="#")
        raw = np.atleast_2d(raw)

        wavelengths = raw[:, 0]
        n_wl = wavelengths.size

        vod = raw[:, 1:].reshape((n_wl, n_tg)).T
        df = pd.DataFrame(vod.T, index=wavelengths,
                          columns=self.output_map.trace_gas.tolist())
        df.columns.name = "Tracegas"
        df.index.name = "Wavelength"

        return df

    def read_wf(self, fn):

        fn = os.path.join(self.path, fn)

        with open(fn, "r") as fd:
            for l in fd.readlines():
                if l.startswith("#"):
                    continue
                altitude = np.asarray(l.split(), dtype=float)
                break

        n_geom = self.output_map.shape[0]
        n_alt = altitude.shape[0]

        raw = np.loadtxt(fn, skiprows=6, comments="#")

        wavelengths = raw[:raw.shape[0] / n_alt, 0]
        n_wl = wavelengths.shape[0]

        bamf = raw[:, 1:].reshape((n_alt, n_wl, n_geom))

        df = pd.Panel(bamf, items=altitude, major_axis=wavelengths,
                      minor_axis=self.output_map.index)
        df.items.name = "Altitude"
        df.major_axis.name = "Wavelength"
        df.minor_axis.name = "Geometry"

        return df

    def read_SCE_ABSORBER(self):
        fn = os.path.join(self.path, "SCE_ABSORBER.OUT")

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
        data = pd.read_csv(fn, sep=str(r"\s+"), skipinitialspace=True,
                           header=None, skiprows=12, skipfooter=6, index_col=0,
                           engine="python")
        # read_csv adds empty column at end; we remove it here
        if data.iloc[:, -1].dropna().shape == (0, ):
            data.drop(data.columns[-1], axis=1, inplace=True)
        try:
            data.columns = names[1:]
        except:
            raise
        return data

    def read_SCE_SUMMARY(self):
        fn = os.path.join(self.path, "SCE_SUMMARY.OUT")
        with open(fn, "r") as fd:
            lines = fd.readlines()
        lines = [l.strip() for l in lines]
        # extract surface information
        summary, current, heading, next_is_heading = {}, [], '', False
        for l in lines:
            if l.startswith('=') and l.endswith('='):
                if current and heading:
                    summary[heading] = current
                current, heading = [], ''
                next_is_heading = True
                continue
            elif l.startswith('-') and l.endswith('-'):
                continue
            elif len(l) == 0:
                continue
            try:
                key, value = l.split(':')
            except ValueError:
                key, value = '', l
            key, value = key.strip(), value.strip()
            if next_is_heading:
                heading = key
                next_is_heading = False
            current.append((key, value))
        for key, value in summary.items():
            for ii, (k, v) in enumerate(value):
                if v.lower() == 'off':
                    value[ii] = k, False
                    continue
                elif v.lower() == 'on':
                    value[ii] = k, True
                    continue
                try:
                    value[ii] = k, float(v)
                except ValueError:
                    pass
            if key == 'SURFACE':
                # TODO: create array from wavelength
                # TODO: create Series from wl-dependent surface
                pass
            try:
                summary[key] = {k: v for k, v in value}
            except:
                raise
        return summary

    def read_local_optical_parameters(self):
        fn_height = os.path.join(self.path, "height.dat")
        height = np.loadtxt(fn_height)
        z_min, z_max = height[1:], height[:-1]
        z_center = (z_min + z_max) / 2.
        if hasattr(self, "intensity"):
            wavelengths = self.intensity.columns.values
        elif hasattr(self, "block_amf"):
            wavelengths = self.block_amf.major_axis.values
        elif hasattr(self, "tg_vod"):
            wavelengths = self.tg_vod.index.values
        else:
            raise ValueError("Cannot determine wavelengths for local optical "
                             "parameters.")

        def _read_one_local_optical_parameter(param):
            fn_data = os.path.join(self.path, "{}.dat".format(param))
            if param == "gas_abs":
                data = np.loadtxt(fn_data)
            elif param == "ray_sca":
                n_z = z_center.size
                n_rows = n_z // 100 + 1  # rows per wavelength
                data = pd.read_csv(fn_data, header=None, delim_whitespace=True)
                data = data.convert_objects(convert_numeric=True).values
                data = [data[i * n_rows:(i + 1) * n_rows].ravel()
                        for i, wl in enumerate(wavelengths)]
                data = np.asarray(data)
                if not np.all(np.isnan(data[:, n_z:])):
                    raise ValueError("Error reading file '{}'".format(fn_data))
                data = data[:, :n_z]
            else:
                raise ValueError("Cannot load local optical parameters for "
                                 "'{}'.".format(param))
            res = pd.DataFrame(data, columns=z_center, index=wavelengths)
            res.columns.name = "Altitude (layer center)"
            res.index.name = "Wavelength"
            return res, (z_min, z_max)

        outdict = dict()

        for param in ["aer_abs", "aer_sca", "cld_abs", "cld_sca", "gas_abs",
                      "ray_sca"]:
            try:
                outdict[param], zz = _read_one_local_optical_parameter(param)
            except ValueError:
                if param == "ray_sca":
                    raise NameError()
                pass
        if len(outdict) == 0:
            raise IOError("No output files for local optical parameters found")

        output = pd.Panel(outdict)
        output["z_min"], output["z_max"] = [np.tile(np.atleast_2d(z), (2, 1))
                                            for z in zz]

        return output
