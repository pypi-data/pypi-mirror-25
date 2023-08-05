# -*- coding: utf-8 -*-
from __future__ import unicode_literals, with_statement, division


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _plot_bamf_series(bamf, ax, label=None, lw=1.):
    """plots a single pd.Series as BAMF"""
    ax.plot(np.asarray(bamf), np.asarray(bamf.index), label=label, lw=lw)
    ax.set_xlim((0., ax.get_xlim()[1]))
    ax.set_xlabel("Block air mass factor (1)")
    ax.set_ylabel("Altitude (km)")


def plot_block_air_mass_factor(bamf, ax=None, labels=None, legend_cols=1,
                               legend_title=None):
    """Create a plot of block air mass factors.

    Parameters
    ----------
    bamf : pandas.DataFrame
        The data to be plotted.  The DataFrame's index must be altitude.

    ax : matplotlib.axes.AxesSubplot
        The axes object to draw the plot in.  By default, a new figure
        will be created.

    labels : list of str, optional
        A list of strings.  By default, the column names from the
        *bamf* DataFrame will be used.

    legend_cols : int, optional
        The number of columns in the legend.  By default, the legend
        will contain 1 column.

    legend_title : str, optional
        The legend title to be written to the plot.  By default, the
        legend will have no title.

    """
    if ax is None:
        fig, ax = plt.subplots()
    if isinstance(bamf, pd.Series):
        _plot_bamf_series(bamf, ax)
    elif isinstance(bamf, pd.DataFrame):
        for i, col in enumerate(bamf.columns):
            label = col if labels is None else labels[i]
            _plot_bamf_series(bamf[col], ax, label=label)
    ax.legend(loc='best', ncol=legend_cols, title=legend_title)
