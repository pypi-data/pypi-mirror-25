from __future__ import division, unicode_literals


import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile


from ..input import save_input_files
from ..params import json_to_sciatran
from ..util import mkbasedir


def run_sciatran(runpath, executable):
    """Run SCIATRAN.

    This function runs the SCIATRAN executable ``excecutable`` in the
    runtime directory ``runpath``.  STDOUT and STDERR of the SCIATRAN
    process are redirected to the files ``stdout.log`` and
    ``stderr.log``, respectively, inside the runtime directory.  After
    termination of the SCIATRAN process, the STDOUT is being checked
    for the string ``***** Normal termination *****``; if this string
    is not found, a *RuntimeError* is raised.

    Parameters
    ----------
    runpath : str
        Path to the runtime directory of SCIATRAN

    executable : str
        Filename of the SCIATRAN executable to run.

    Notes
    -----
    This function assumes that the runtime directory ``runpath`` has
    been properly set up beforehand.

    """
    if executable is None:
        raise NotImplementedError()
    stdout = os.path.join(runpath, "stdout.log")
    stderr = os.path.join(runpath, "stderr.log")
    # run SCIATRAN
    with open(stdout, "a") as fd_stdout, open(stderr, "a") as fd_stderr:
        subprocess.check_call(["./{}".format(executable)],
                              cwd=runpath, stdout=fd_stdout,
                              stderr=fd_stderr)
    # check if SCIATRAN terminated normally
    pattern_normal = re.compile("\*\*\*\*\* Normal termination \*\*\*\*\*")
    normal_termination = False
    with open(stdout, "r") as fd_stdout:
        for line in fd_stdout:
            if pattern_normal.search(line):
                normal_termination = True
                break
    if not normal_termination:
        raise RuntimeError("SCIATRAN did not terminate normally!")


def setup_runtime(cfg, sciaexec, dirname=None, basepath="/tmp", clean=True,
                  symlink_exec=False):
    """Setup a runtime directory for SCIATRAN.

    This function will prepare a new runtime directory for SCIATRAN,
    given the configuration dict ``cfg``.  It will perform the following
    steps:

    1. create the runtime directory, if necessary
    2. clean the runtime directory from previous output files, if
       requested by the ``clean`` parameter
    3. create folders ``DATA_IN`` and ``DATA_OUT`` inside the runtime
       directory
    4. copy the SCIATRAN executable ``sciaexec`` to the runtime directory
    5. copy all required input files (e.g., profiles, cross-sections,
       ...) to the folder ``DATA_IN``, and update the runtime
       configuration accordingly
    6. create SCIATRAN parameter files from the updated runtime
       configuration ``cfg`` and store them in the runtime directory
    7. save SCIATRAN configuration as ``sciaconf.json`` in the runtime
       directory

    Parameters
    ----------
    cfg : dictionary
        The configuration from which the SCIATRAN parameter files
        (``*.inp``) shall be generated.

    sciaexec : str
        Path to the SCIATRAN executable which shall be copied to the
        runtime directory.

    dirname : str, optional
        Name of the runtime directory to be created.  Defaults to a
        random name.

    basepath : str, optional
        Directory in which the runtime directory is to be created.
        Defaults to ``/tmp``.

    clean : bool, optional
        If *True*, the runtime directory, if existing, will be cleaned
        of all output and log files.  Defaults to *False*.

    symlink_exec : bool, optional
        If *True*, the SCIATRAN executable will be sym-linked into the
        runtime directory; if *False*, the file will be physically
        copied.  Defaults to *False*.

    Returns
    -------
    runpath : str
        Full path to the runtime directory created.

    """
    # check SCIATRAN executable
    md5_desired = cfg.get("sciatran_md5")
    if md5_desired:
        with open(sciaexec, "rb") as fd_scia:
            md5_actual = hashlib.md5(fd_scia.read()).hexdigest()
        if md5_desired != md5_actual:
            raise ValueError("The given SCIATRAN executable does not have the "
                             "required MD5 hash. Please ensure that you are "
                             "actually using the correct SCIATRAN executable, "
                             "or update the MD5 hash in your runtime "
                             "configuration accordingly.")

    if dirname is None:
        runpath = tempfile.mkdtemp(dir=basepath)
    else:
        runpath = os.path.join(basepath, dirname)
    # clean up
    if clean:
        for out in glob.glob(os.path.join(runpath, "DATA_OUT", "*")):
            os.remove(out)
        for log in glob.glob(os.path.join(runpath, "*.log")):
            os.remove(log)
    # create in-/output directories
    for outname in ["DATA_OUT", "DATA_IN"]:
        try:
            os.makedirs(os.path.join(runpath, outname))
        except OSError:  # directory already exists
            pass
    # copy SCIATRAN executable
    if symlink_exec:
        os.symlink(sciaexec, os.path.join(runpath, os.path.basename(sciaexec)))
    else:
        shutil.copy(sciaexec, runpath)
    # copy input files into DATA_IN, adapt Param paths accordingly
    runcfg = save_input_files(cfg, runpath)
    # save SCIATRAN parameters
    json_to_sciatran(runcfg, runpath)
    with open(os.path.join(runpath, "sciaconf.json"), 'w') as outfile:
        json.dump(runcfg, outfile)
    return runpath


def store_results(runpath, target, save_inputs=True, save_executable=True,
                  create_dirs=True):
    """Store SCIATRAN runtime in ZIP format.

    By default, the full runtime directory will be stored, ensuring
    full reproducibility of the SCIATRAN run.

    Parameters
    ----------
    runpath : str
        The SCIATRAN runtime directory to be saved.

    target : str
        The zip file to be created.

    save_inputs : bool, optional
        If *True*, the input files from the directory ``DATA_IN`` will
        be stored in the zipfile.  Defaults to *True*.

    save_executable : bool, optional
        If *True*, the SCIATRAN executable will be stored in the
        zipfile.  Defaults to *True*.

    create_dirs : bool, optional
        If *True*, automatically create all directories so that the
        output file can be created at *target*.

    Notes
    -----
    The kwarg *save_executable* treats any file inside the runtime
    directory which is not contained in ``DATA_IN``, ``DATA_OUT``, or
    does not end in ``.inp`` or ``.log`` as executable.  While this is
    not optimal, it is the only way to definitely not miss the
    executable.

    """
    if create_dirs:
        mkbasedir(target)

    with zipfile.ZipFile(target, "w",
                         compression=zipfile.ZIP_DEFLATED) as Z:
        for root, dirs, files in os.walk(runpath):
            for f in files:
                abspath = os.path.join(root, f)
                if os.path.split(os.path.dirname(abspath))[1] == "DATA_IN":
                    if not save_inputs:
                        continue
                elif not (os.path.splitext(abspath)[1] in [".inp", ".log",
                                                           ".json"] or
                          (os.path.split(os.path.dirname(abspath))[1] ==
                           "DATA_OUT")):
                    # this must be the executable ...
                    if not save_executable:
                        continue
                Z.write(abspath, os.path.relpath(abspath, runpath))
