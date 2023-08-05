# -*- coding: utf-8 -*-
"""
*****************************************************************************
pyatran - Handling SCIATRAN
*****************************************************************************

:Author:    Andreas Hilboll <hilboll@uni-bremen.de>
:Date:      Fri 27 Mar 2014

"""

from setuptools import setup


import versioneer


if __name__ == "__main__":
    setup(
        name='pyatran',
        description=(
            'Python tools for working with the SCIATRAN radiative transfer '
            'model'),
        url='https://gitlab.com/andreas-h/pyatran/',
        author='Andreas Hilboll',
        author_email='hilboll@uni-bremen.de',
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        install_requires=[
            'numpy>=1.7', 'pandas>=0.15', 'xarray>=0.9', 'matplotlib>=1.4.1'],
        tests_require=[
            'pytest', 'pytest-flake8', 'pytest-cov', 'pytest-runner'],
        license='AGPLv3',
        classifiers=[
            # How mature is this project? Common values are
            'Development Status :: 4 - Beta',
            # Indicate who your project is intended for
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering :: Atmospheric Science',
            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: GNU Affero General Public License v3',
            # Specify the Python versions you support here. In particular,
            # ensure that you indicate whether you support Python 2, Python 3
            # or both.
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            # Specify operating system
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
        ],
        packages=[
            'pyatran',
            'pyatran.input',
            'pyatran.output',
            'pyatran.params',
            'pyatran.plot',
            'pyatran.runtime',
            'pyatran.util',
        ]
    )
