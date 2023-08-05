# -*- coding: utf-8 -*-
# Copyright (c) 2015, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Definition of some common methods that might be useful.

Important methods defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

inspect_function (:py:func:`.inspect_function`)
    A method to obtain information about arguments, keyword arguments
    for functions.

initiate_instance (:py:func:`.initiate_instance`)
    Method to initiate a class with optional arguments.

generic_factory (:py:func:`.generic_factory`)
    Create instances of classes based on settings.
"""
import logging
import inspect
from pyretis.core.path import Path, PathExt
from pyretis.core.reservoirpath import ReservoirPath


logger = logging.getLogger(__name__)  # pylint: disable=C0103
logger.addHandler(logging.NullHandler())


__all__ = ['inspect_function', 'initiate_instance', 'generic_factory']


def _arg_kind(arg):
    """Helper function to determine kind for a given argument.

    This method will help :py:func:`.inspect_function` to determine
    the correct kind for arguments when using python3.

    Parameters
    ----------
    arg : object like :py:class:`inspect.Parameter`.
        The argument we will determine the type of.

    Returns
    -------
    out : string
        A string we use for determine the kind.
    """
    kind = None
    if arg.kind == arg.POSITIONAL_OR_KEYWORD:
        if arg.default is arg.empty:
            kind = 'args'
        else:
            kind = 'kwargs'
    elif arg.kind == arg.POSITIONAL_ONLY:
        kind = 'args'
    elif arg.kind == arg.VAR_POSITIONAL:
        kind = 'varargs'
    elif arg.kind == arg.VAR_KEYWORD:
        kind = 'keywords'
    elif arg.kind == arg.KEYWORD_ONLY:
        # we treat these as keyword arguments:
        kind = 'kwargs'
    return kind


def inspect_function(function):
    """Method returning arguments/kwargs of a given function.

    This method is intended for usage where we are checking that we can
    call certain function. This method will return arguments and
    keyword arguments a function expects. This method may be fragile -
    we assume here that we are not really interested in args and
    kwargs and we do not look for more information about these here.

    Parameters
    ----------
    function : callable
        The function to analyse.

    Returns
    -------
    out : dict
        A dict with the arguments, the following keys are defined:

        * `args` : list of the positional arguments
        * `kwargs` : list of keyword arguments
        * `varargs` : list of arguments
        * `keywords` : list of keyword arguments
    """
    out = {'args': [], 'kwargs': [],
           'varargs': [], 'keywords': []}
    arguments = inspect.signature(function)  # pylint: disable=no-member
    for arg in arguments.parameters.values():
        kind = _arg_kind(arg)
        if kind is not None:
            out[kind].append(arg.name)
        else:  # pragma: no cover
            logger.critical('Unknown variable kind "%s" for "%s"',
                            arg.kind, arg.name)
    return out


def _pick_out_arg_kwargs(klass, settings):
    """Method to pick out arguments for a class from settings.

    Parameters
    ----------
    klass : class
        The class to initiate.
    settings : dict
        Positional and keyword arguments to pass to `klass.__init__()`.

    Returns
    -------
    out[0] : list
        A list of the positional arguments.
    out[1] : dict
        The keyword arguments.
    """
    info = inspect_function(klass.__init__)
    used, args, kwargs = set(), [], {}
    for arg in info['args']:
        if arg == 'self':
            continue
        try:
            args.append(settings[arg])
            used.add(arg)
        except KeyError:
            msg = 'Required argument "{}" for "{}" not found!'.format(arg,
                                                                      klass)
            raise ValueError(msg)
    for arg in info['kwargs']:
        if arg == 'self':
            continue
        if arg in settings:
            kwargs[arg] = settings[arg]
    return args, kwargs


def initiate_instance(klass, settings):
    """Method to initiate a class with optional arguments.

    Parameters
    ----------
    klass : class
        The class to initiate.
    settings : dict
        Positional and keyword arguments to pass to `klass.__init__()`.

    Returns
    -------
    out : instance of `klass`
        Here, we just return the initiated instance of the given class.
    """
    args, kwargs = _pick_out_arg_kwargs(klass, settings)
    # Ready to initiate!
    msg = 'Initiated "%s" from "%s" %s'
    name = klass.__name__
    mod = klass.__module__
    if not args:
        if not kwargs:
            logger.debug(msg, name, mod, 'without arguments.')
            return klass()
        logger.debug(msg, name, mod, 'with keyword arguments.')
        return klass(**kwargs)
    if not kwargs:
        logger.debug(msg, name, mod, 'with positional arguments.')
        return klass(*args)
    logger.debug(msg, name, mod,
                 'with positional and keyword arguments.')
    return klass(*args, **kwargs)


def generic_factory(settings, object_map, name='generic'):
    """Create instances of classes based on settings.

    This method is intended as a semi-generic factory for creating
    instances of different objects based on simulation input settings.
    The input settings defines what classes should be created and
    the object_map defines a mapping between settings and the
    class.

    Parameters
    ----------
    settings : dict
        This defines how we set up and select the order parameter.
    object_map : dict
        Definitions on how to initiate the different classes.
    name : string
        Short name for the object type. Only used for error messages.

    Returns
    -------
    out : instance of a class
        The created object, in case we were successful. Otherwise we
        return none.
    """
    try:
        klass = settings['class'].lower()
    except KeyError:
        msg = 'No class given for %s -- could not create object!'
        logger.critical(msg, name)
        return None
    if klass not in object_map:
        logger.critical('Could not create unknown class "%s" for %s',
                        settings['class'], name)
        return None
    cls = object_map[klass]['cls']
    return initiate_instance(cls, settings)


def get_path_class(ensemble_type):
    """Method to return the path class to work with an integrator.

    Parameters
    ----------
    ensemble_type : string
        The type of ensemble we are requesting.

    Returns
    -------
    out : object like :py:class:`.PathBase`
        A path we can fill :-)
    """
    path_map = {'internal': Path,
                'external': PathExt,
                'reservoir': ReservoirPath}
    try:
        klass = path_map[ensemble_type]
        return klass
    except KeyError:
        msg = 'Unknown ensemble type "{}" requested.'.format(ensemble_type)
        logger.critical(msg)
        raise ValueError(msg)
