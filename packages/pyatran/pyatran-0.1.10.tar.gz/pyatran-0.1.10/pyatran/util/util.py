# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import errno


__all__ = ["mkbasedir"]


def mkbasedir(path, check=False):
    """Create directory needed to create a file.

    This function creates the base directory of the file/folder
    located at *path*.

    Parameters
    ----------
    path : str
        Path of file, whose base directory shall be created.

    check : bool, optional
        If *True*, raise an Exception if the directory already exists.
        If *False*, silently do nothing.

    Notes
    -----
    This function is identical to ``IUPy.util.file_io.mkbasedir`` but is
    included explicitly in pyatran to avoid dependencies.

    """
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)))
    except OSError as err:
        if (err.errno == errno.EEXIST) and not check:
            pass
