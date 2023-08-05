# -*- coding: utf-8 -*-
# Copyright (c) 2015, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""This file contains common functions for the input/output.

It contains some functions that is used when generating reports,
typically to format tables and numbers.

Important classes defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PyretisLogFormatter (:py:class:`.PyretisLogFormatter`)
    A class representing a formatter for the PyRETIS log file.

Important methods defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

apply_format (:py:func:`.apply_format`)
    Apply a format string to a given float value. This method
    can be used for formatting text for tables (i.e. if we want
    a fixed width).

check_python_version (:py:func:`.check_python_version`)
    Method that will give warnings when we use older and untested
    versions of python.

create_backup (:py:func:`.create_backup`)
    A function to handle the creation of backups of old files.

make_dirs (:py:func:`.make_dirs`)
    Create directories (for path simulation).

print_to_screen (:py:func:`.print_to_screen`)
    A method used for printing to screen.
"""
import errno
import os
import re
import sys
import logging
import colorama
logger = logging.getLogger(__name__)  # pylint: disable=C0103
logger.addHandler(logging.NullHandler())


__all__ = ['apply_format', 'check_python_version', 'create_backup',
           'make_dirs', 'print_to_screen', 'PyretisLogFormatter']


# Hard-coded patters for energy analysis output files.
# These are just used to make it simpler to change these default
# names in the future.
ENERFILES = {'energies': 'energies',
             'run_energies': 'runenergies',
             'temperature': 'temperature',
             'run_temp': 'runtemperature',
             'block': '{}block',
             'dist': '{}dist'}
# hard-coded information for the energy terms:
ENERTITLE = {'vpot': 'Potential energy',
             'ekin': 'Kinetic energy',
             'etot': 'Total energy',
             'ham': 'Hamilt. energy',
             'temp': 'Temperature',
             'elec': 'Energy (externally computed)'}
# hard-coded patters for flux analysis output files:
FLUXFILES = {'runflux': 'runflux_{}',
             'block': 'errflux_{}'}
# order files:
ORDERFILES = {'order': 'order',
              'ordervel': 'orderv',
              'run_order': 'runorder',
              'dist': 'orderdist',
              'block': 'ordererror',
              'msd': 'ordermsd'}
# hard-coded patters for path analysis output files:
PATHFILES = {'pcross': '{}_pcross',
             'prun': '{}_prun',
             'perror': '{}_perror',
             'lengtherror': '{}_lerror',
             'pathlength': '{}_lpath',
             'shoots': '{}_shoots',
             'shoots_scaled': '{}_shoots_scaled'}
# hard-coded patterns for matched files:
PATH_MATCH = {'total': 'total-probability',
              'match': 'matched-probability'}
# hard-coded formats to use for Log files:
LOG_FMT = '[%(levelname)s]: %(message)s'
LOG_DEBUG_FMT = '[%(levelname)s] [%(name)s.%(funcName)s()]: %(message)s'
# colors for printing:
COLORS = {'error': colorama.Fore.RED,
          'info': colorama.Fore.BLUE,
          'warning': colorama.Fore.YELLOW,
          'message': colorama.Fore.CYAN,
          'success': colorama.Fore.GREEN}


def create_backup(outputfile):
    """Check if a file exist and create backup if requested.

    This function will check if the given file name exist and if it
    does, it will move that file to a new file name such that the given
    one can be used without overwriting.

    Parameters
    ----------
    outputfile : string
        This is the name of the file we wish to create.

    Returns
    -------
    out : string
        This string is None if no backup is made, otherwise it will just
        say what file was moved (and to where).

    Note
    ----
    No warning is issued here. This is just in case the `msg` returned
    here will be part of some more elaborate message.
    """
    filename = '{}'.format(outputfile)
    fileid = 0
    msg = None
    while os.path.isfile(filename) or os.path.isdir(filename):
        filename = '{}_{:03d}'.format(outputfile, fileid)
        fileid += 1
    if fileid > 0:
        msg = 'Backup existing file "{}" to "{}"'.format(outputfile, filename)
        os.rename(outputfile, filename)
    return msg


def apply_format(value, fmt):
    """Apply a format string to a given float value.

    Here we check the formatting of a float. We are *forcing* a
    *maximum length* on the resulting string. This is to avoid problems
    like: '{:7.2f}'.format(12345.7) which returns '12345.70' with a
    length 8 > 7. The intended use of this function is to avoid such
    problems when we are formatting numbers for tables. Here it is done
    by switching to an exponential notation. But note however that this
    will have implications for how many decimal places we can show.

    Parameters
    ----------
    value : float
        The float to format.
    fmt : string
        The format to use.

    Note
    ----
    This function converts numbers to have a fixed length. In some
    cases this may reduce the number of significant digits. Remember
    to also output your numbers without this format in case a specific
    number of significant digits is important!
    """
    maxlen = fmt.split(':')[1].split('.')[0]
    align = ''
    if not maxlen[0].isalnum():
        align = maxlen[0]
        maxlen = maxlen[1:]
    maxlen = int(maxlen)
    str_fmt = fmt.format(value)
    if len(str_fmt) > maxlen:  # switch to exponential:
        if value < 0:
            deci = maxlen - 7
        else:
            deci = maxlen - 6
        new_fmt = '{{:{0}{1}.{2}e}}'.format(align, maxlen, deci)
        return new_fmt.format(value)
    else:
        return str_fmt


def _remove_extension(filename):
    """Remove the extension of a given file name.

    Parameters
    ----------
    filename : string
        The file name to check.

    Returns
    -------
    out : string
        The filename with the extension removed.
    """
    try:
        return os.path.splitext(filename)[0]
    except IndexError:  # pragma: no cover
        return filename


def make_dirs(dirname):
    """Create directories for path simulations.

    This function will create a folder using a specified path.
    If the path already exist and if it's a directory, we will do
    nothing. If the path exist and is a file we will raise an
    `OSError` exception here.

    Parameters
    ----------
    dirname : string
        This is the directory to create.

    Returns
    -------
    out : string
        A string with some info on what this function did. Intended for
        output.
    """
    try:
        os.makedirs(dirname)
        msg = 'Created directory: "{}"'.format(dirname)
        return msg
    except OSError as err:
        if err.errno != errno.EEXIST:  # pragma: no cover
            raise err
        if os.path.isfile(dirname):
            msg = '"{}" is a file. Will abort!'
            raise OSError(errno.EEXIST, msg, dirname)
        if os.path.isdir(dirname):
            msg = 'Directory "{}" already exist.'.format(dirname)
            return msg


def print_to_screen(txt=None, level=None):  # pragma: no cover
    """Method to print output to standard out.

    This method is included to ensure that output from PyRETIS to the
    screen is written out in a uniform way across the library and
    application(s).

    Parameters
    ----------
    txt : string
        The text to write to the screen.
    level : string
        The level can be used to color the output.
    """
    if txt is None:
        print()
    else:
        out = '{}'.format(txt)
        color = COLORS.get(level, None)
        if color is None:
            print(out)
        else:
            print(color + out)


def simplify_ensemble_name(ensemble, fmt='{:03d}'):
    """A function to simplify path names for file/directory names.

    Here, we are basically translating ensemble names to more friendly
    names for directories and files that is:

    - ``[0^-]`` returns ``000``,
    - ``[0^+]`` returns ``001``,
    - ``[1^+]`` returns ``002``, etc.

    Parameters
    ----------
    ensemble : string
        This is the string to translate
    fmt : string. optional
        This is a format to use for the directories.
    """
    match_ensemble = re.search(r'(?<=\[)(\d+)(?=\^)', ensemble)
    if match_ensemble:
        ens = int(match_ensemble.group())
    else:
        match_ensemble = re.search(r'(?<=\[)(\d+)(?=\])', ensemble)
        if match_ensemble:
            ens = int(match_ensemble.group())
        else:
            return ensemble  # Assume that the ensemble is OK as it is.
    match_dir = re.search(r'(?<=\^)(.)(?=\])', ensemble)
    if match_dir:
        dire = match_dir.group()
        if dire == '-':
            ens = ens
        else:
            ens += 1
    else:
        msg = ['Could not get direction for ensemble {}.'.format(ensemble),
               'We assume "+", note that this might overwrite files']
        logger.warning('\n'.join(msg))
        ens += 1
    return fmt.format(ens)


def add_dirname(filename, dirname):
    """Add a directory as a prefix to a filename, i.e. `dirname/filename`.

    Parameters
    ----------
    filename : string
        The filename.
    dirname : string
        The directory we want to prefix. It can be None, in which
        case we ignore it.

    Returns
    -------
    out : string
        The path to the resulting file.
    """
    if dirname is not None:
        return os.path.join(dirname, filename)
    return filename


def name_file(name, extension, path=None):
    """Return a file name by joining a name and an file extension.

    This function is used to create file names. It will use
    `os.extsep` to create the file names and `os.path.join` to add a
    path name if the `path` is given. The returned file name fill be of
    form (example for posix): ``path/name.extension``.

    Parameters
    ----------
    name : string
        This is the name, without extension, for the file.
    extension : string
        The extension to use for the file name.
    path : string, optional
        An optional path to add to the file name.

    Returns
    -------
    out : string
        The resulting file name
    """
    return add_dirname(os.extsep.join([name, extension]), path)


def check_python_version():  # pragma: no cover
    """Method that will give a warning about old python version(s)."""
    pyversion = sys.version.split()[0]
    if sys.version_info < (3, 0):
        msgtxt = ('Please upgrade to Python 3.'
                  '\nPython {} is not supported!')
        msgtxt = msgtxt.format(pyversion)
        logger.error(msgtxt)
        raise SystemExit(msgtxt)


class PyretisLogFormatter(logging.Formatter):  # pragma: no cover
    """Hard-coded formatter for the PyRETIS log file.

    This formatter will just adjust multi-line messages to have some
    indentation.
    """
    def format(self, record):
        out = logging.Formatter.format(self, record)
        header, _ = out.split(record.message)
        out = out.replace('\n', '\n' + ' ' * len(header))
        return out


def format_number(number, minf, maxf, fmtf='{0:<16.9f}', fmte='{0:<16.9e}'):
    """Method to format a number based on it's size.

    Parameters
    ----------
    number : float
        The number to format.
    minf : float
        If the number is smaller than `minf` then apply the
        format with scientific notation.
    maxf : float
        If the number is greater than `maxf` then apply the
        format with scientific notation.
    fmtf : string
        Format to use for floats.
    fmte : string
        Format to use for scientific notation.

    Returns
    -------
    out : string
        The formatted number."""
    if minf <= number <= maxf:
        return fmtf.format(number)
    return fmte.format(number)


def get_log_formatter(level):
    """Helper function to select a log format.

    Here, it is just used to get a slightly more verbose format for
    the debug level.

    Parameters
    ----------
    level : integer
        This integer defines the log level.

    Returns
    -------
    out : object like :py:class:`logging.Formatter`
        An object that can be used as a formatter for a logger.
    """
    if level <= logging.DEBUG:
        return PyretisLogFormatter(LOG_DEBUG_FMT)
    return PyretisLogFormatter(LOG_FMT)
