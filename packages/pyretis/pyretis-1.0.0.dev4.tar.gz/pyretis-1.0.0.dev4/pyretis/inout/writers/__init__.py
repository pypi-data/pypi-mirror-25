# -*- coding: utf-8 -*-
# Copyright (c) 2015, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This sub-package handle writers for PyRETIS data.

Writers are basically formatting the data created from PyRETIS.
The writers also have some additional functionality and can be used to
load data written by PyRETIS as well. This is used when analysing
the output from a PyRETIS simulation.

Package structure
-----------------

Modules
~~~~~~~

cp2k.py (:py:mod:`pyretis.inout.writers.cp2kio`)
    Module for handling input/output from CP2K.

fileio.py (:py:mod:`pyretis.inout.writers.fileio`)
    Module defining a class for handling writing of files.

gromacsio.py (:py:mod:`pyretis.inout.writers.gromacsio`)
    Module defining some io methods for use with GROMACS.

__init__.py
    This file.

pathfile.py (:py:mod:`pyretis.inout.writers.pathfile`)
    Module for handling path data and path-ensemble data.

tablewriter.py (:py:mod:`pyretis.inout.writers.tablewriter`)
    Module defining generic methods for creating text tables.

txtinout.py (:py:mod:`pyretis.inout.writers.txtinout`)
    Module defining some text based output.

writers.py (:py:mod:`pyretis.inout.writers.writers`)
    Module for defining the base writer and some simple derived writers
    (for crossing data, energy and order parameter data).

xyzio.py (:py:mod:`pyretis.inout.writers.xyzio`)
    Module for handling writing of trajectory data in XYZ format.

Important methods defined in this package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

get_writer (:py:func:`.get_writer`)
    Opens a file for reading given a file type and file name.

prepare_load (:py:func:`.prepare_load`)
    Open up a file for reading, given file type and file name, and
    create the generator for it. This method can be set to fail if
    the file is not found.

Important classes defined in this package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CrossWriter (:py:class:`.CrossWriter`)
    A writer of crossing data.

EnergyWriter (:py:class:`.EnergyWriter`)
    A writer of energy data

EnergyPathWriter (:py:class:`.EnergyPathWriter`)
    A class for writing out energy data for paths.

OrderWriter (:py:class:`.OrderWriter`)
    A writer of order parameter data.

OrderPathWriter (:py:class:`.OrderPathWriter`)
    A class for writing out order parameter data for paths.

TrajWriter (:py:class:`.TrajWriter`)
    Generic class for writing trajectory output.

PathExtWriter (:py:class:`.PathExtWriter`)
    A class for writing external paths to file.

PathIntWriter (:py:class:`.PathIntWriter`)
    A class for writing internal paths to file.

PathEnsembleWriter (:py:class:`.PathEnsembleWriter`)
    A writer of path ensemble data.

PathEnsembleFile (:py:class:`.PathEnsembleFile`)
    A class which represent path ensembles in files. This class is
    intended for use in an analysis.

TxtTable (:py:class:`.TxtTable`)
    A generic table writer.

ThermoTable (:py:class:`.ThermoTable`)
    A specific table writer for energy output.

PathTable (:py:class:`.PathTable`)
    A specific table writer for path results.
"""
import logging
import os
import errno
from pyretis.core.common import initiate_instance
from .fileio import FileIO
from .pathfile import PathEnsembleWriter, PathEnsembleFile
from .tablewriter import TxtTable, ThermoTable, PathTable
from .writers import (CrossWriter,
                      EnergyWriter, EnergyPathWriter,
                      OrderWriter, OrderPathWriter,
                      TrajWriter, PathExtWriter, PathIntWriter)

logger = logging.getLogger(__name__)  # pylint: disable=C0103
logger.addHandler(logging.NullHandler())


_CLASS_MAP = {'cross': CrossWriter,
              'order': OrderWriter,
              'energy': EnergyWriter,
              'pathensemble': PathEnsembleWriter,
              'thermotable': ThermoTable,
              'trajtxt': TrajWriter,
              'pathtable': PathTable,
              'pathorder': OrderPathWriter,
              'pathenergy': EnergyPathWriter,
              'pathtrajint': PathIntWriter,
              'pathtrajext': PathExtWriter}


def get_writer(file_type, settings=None):
    """Return a file object which can be used for loading files.

    This is a convenience function to return an instance of a `Writer`
    or derived classes so that we are ready to read data from that file.
    Usage is intended to be in cases when we just want to open a file
    easily. The returned object can then be used to read the file
    using `load(filename)`.

    Parameters
    ----------
    file_type : string
        The desired file type
    settings : dict
        A dict of settings we might need to pass for to the writer.
        This can for instance be the units for a trajectory writer.

    Returns
    -------
    out : object like :py:class:`.Writer`
        An object which implements the `load(filename)` method.

    Examples
    --------
    >>> from pyretis.inout.writers import get_writer
    >>> crossfile = get_writer('cross')
    >>> print(crossfile)
    >>> for block in crossfile.load('cross.dat'):
    >>>     print(len(block['data']))
    """
    try:
        cls = _CLASS_MAP[file_type]
        if settings is None:
            return initiate_instance(cls, {})
        return initiate_instance(cls, settings)
    except KeyError:
        msg = 'Unknown file type {} requested. Ignored'.format(file_type)
        logger.error(msg)
        return None


def prepare_load(file_type, filename, required=True):
    """Prepare to load a file of a given file type

    Parameters
    ----------
    file_type : string
        This selects the file type.
    filename : string
        The path to the file we are to open.
    required : boolen
        If True, we will fail if we can't find the file.

    Returns
    -------
    out : generator or None
        A generator which can be used to read the file.
    """
    if not os.path.isfile(filename):
        if required:
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                filename
            )
        else:
            return None
    else:
        loader = get_writer(file_type)
        if loader is None:
            raise ValueError('Could not open type: "{}"'.format(file_type))
        else:
            return loader.load(filename)
