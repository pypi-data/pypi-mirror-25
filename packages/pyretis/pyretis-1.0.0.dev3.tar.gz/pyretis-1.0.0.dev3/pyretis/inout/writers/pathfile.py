# -*- coding: utf-8 -*-
# Copyright (c) 2015, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Methods and classes for input/output of path data.

This module defines classes for writing path ensemble data.

Important classes defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PathEnsembleWriter (:py:class:`.PathEnsembleWriter`)
    Writing/reading of path ensemble data.

PathEnsembleFile (:py:class:`.PathEnsembleFile`)
    Reading of path ensemble data. Mainly used for analysis.
"""
import logging
from pyretis.core.pathensemble import PathEnsemble
from pyretis.inout.writers.writers import Writer
logger = logging.getLogger(__name__)  # pylint: disable=C0103
logger.addHandler(logging.NullHandler())


__all__ = ['PathEnsembleWriter', 'PathEnsembleFile']


class PathEnsembleWriter(Writer):
    """A class for writing path ensemble data.

    This class handles writing/reading of path ensemble data to a file.

    In the future, this should be made smarter, for instance could path
    data be read in portions, or the full path file could be read if
    it's small enough to fit in the memory. A line-by-line analysis as
    it is right now might not be the most efficient way.
    """
    # Define a format used for the path files. Here it's not really needed,
    # we are going to assume that these files will be comma separated anyway.
    # It is included to be compatible with the old FORTRAN program (TISMOL).
    PATH_FMT = ('{0:>10d} {1:>10d} {2:>10d} {3:1s} {4:1s} {5:1s} {6:>7d} ' +
                '{7:3s} {8:2s} {9:>16.9e} {10:>16.9e} {11:>7d} {12:>7d} ' +
                '{13:>16.9e} {14:>7d} {15:7d}')

    def __init__(self):
        """Initialise the `PathEnsembleWriter`."""
        header = {'labels': ['Step', 'No. acc', 'No. shoot',
                             'l', 'm', 'r', 'Length', 'Acc', 'Mc',
                             'Min-O', 'Max-O', 'Idx-Min', 'Idx-Max',
                             'O-shoot', 'Idx-sh', 'Idx-shN'],
                  'width': [10, 10, 10, 1, 1, 1, 7, 3, 2, 16, 16, 7, 7,
                            16, 7, 7]}
        super().__init__('PathEnsembleWriter', header=header)

    @staticmethod
    def line_parser(line):
        """Convert a text line to simplified representation of a path.

        This is used to parse a file with path data. It will not
        create a real `pyretis.core.path.Path` objects but only a dict
        with information about this path. This dict can be used to
        build up a path ensemble.

        Parameters
        ----------
        line : string
            The line of text to convert.

        Returns
        -------
        out : dict
            This dict contains the path information.
        """
        if line.find('#') != -1:
            linec = line.split('#')[0].strip()
        else:
            linec = line.strip()
        data = [col.strip() for col in linec.split()]
        if len(data) < 16:  # valid data should have 15 columns!
            return None
        path_info = {'cycle': int(data[0]),
                     'generated': [str(data[8]), float(data[13]),
                                   int(data[14]), int(data[15])],
                     'status': str(data[7]),
                     'length': int(data[6]),
                     'ordermax': (float(data[10]), int(data[12])),
                     'ordermin': (float(data[9]), int(data[11]))}
        start = str(data[3])
        middle = str(data[4])
        end = str(data[5])
        path_info['interface'] = (start, middle, end)
        return path_info

    def load(self, filename):
        """Yield the different paths stored in the file.

        The lines are read on-the-fly, converted and yielded one-by-one.
        Note that the file will be opened and closed here.

        Parameters
        ----------
        filename : string
            The path/filename to open.

        Yields
        ------
        out : object like :py:class:`.Path`
            The current path in the file.
        """
        try:
            with open(filename, 'r') as fileh:
                for line in fileh:
                    path_data = self.line_parser(line)
                    if path_data is not None:
                        yield path_data
        except IOError as error:
            msg = 'I/O error ({}): {}'.format(error.errno, error.strerror)
            logger.critical(msg)
        except Exception as error:
            msg = 'Error: {}'.format(error)
            logger.critical(msg)
            raise

    def generate_output(self, cycle, path_ensemble):
        """Generate the output for the path ensemble writer

        The latest path from the path ensemble will be written.

        Parameters
        ----------
        cycle : integer
            This is the current cycle number.
        path_ensemble : object like :py:class:`.PathEnsemble`
            We will write the path defined by ``PathEnsemble.paths[-1]``

        Yields
        ------
        out : string
            The line(s) to be written
        """
        path_dict = path_ensemble.paths[-1]

        interface_list = []
        for val in path_dict['interface']:
            if val is None:
                interface_list.append('*')
            else:
                interface_list.append(val)

        out = self.PATH_FMT.format(cycle,
                                   path_ensemble.nstats['ACC'],
                                   path_ensemble.nstats['nshoot'],
                                   interface_list[0],
                                   interface_list[1],
                                   interface_list[2],
                                   path_dict['length'],
                                   path_dict['status'],
                                   path_dict['generated'][0],
                                   path_dict['ordermin'][0],
                                   path_dict['ordermax'][0],
                                   path_dict['ordermin'][1],
                                   path_dict['ordermax'][1],
                                   path_dict['generated'][1],
                                   path_dict['generated'][2],
                                   path_dict['generated'][3])
        yield out


class PathEnsembleFile(PathEnsemble, PathEnsembleWriter):
    """A class for writing path ensemble data to files.

    This class is intended to mimic the `PathEnsemble` class but
    using files. It overloads the `get_paths()` from the PathEnsemble
    so that the analysis can be run on this object in the same way
    that it is run on a `PathEnsemble` object. This object is included
    as a convenient way of interacting with a path ensemble file
    without having to load the entire file into memory. The
    `PathensembleWriter` does not include a reference to a file name
    but we do that in this class. We can then use the `load()` function
    to iterate over paths in the file.

    Attributes
    ----------
    filename : string
        The file we are going to read.
    """

    def __init__(self, filename, ensemble, interfaces, detect=None):
        """Initiate the `PathEnsembleFile`.

        Parameters
        ----------
        filename : string
            The file we are working with.
        ensemble : integer
            An integer which identifies the ensemble.
        interfaces : list of floats
            The interfaces defining the ensemble.
        detect : float
            The detect interface for this ensemble.
        """
        PathEnsemble.__init__(self, ensemble, interfaces, detect=detect)
        PathEnsembleWriter.__init__(self)
        self.filename = filename

    def get_paths(self):
        """Load paths from the file."""
        for path in self.load(self.filename):
            yield path
