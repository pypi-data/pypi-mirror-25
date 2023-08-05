# -*- coding: utf-8 -*-
# Copyright (c) 2015, PyRETIS Development Team.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Definition of order parameters.

This package defines order parameters for use with PyRETIS.


Package structure
-----------------

Modules
~~~~~~~

orderparameter.py (:py:mod:`pyretis.orderparameter.orderparameter`)
    Defines the base class for order parameters and some simple
    example order parameters.

Important methods defined here
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

order_factory (:py:func:`.order_factory`)
    A method to create order parameters from settings.
"""
from pyretis.core.common import generic_factory
from .orderparameter import (OrderParameter,
                             OrderParameterPosition,
                             OrderParameterDistance)
from .orderangle import OrderParameterAngle
from .orderdihedral import OrderParameterDihedral


def order_factory(settings):
    """Create order parameters according to the given settings.

    This function is included as a convenient way of setting up and
    selecting the order parameter.

    Parameters
    ----------
    settings : dict
        This defines how we set up and select the order parameter.

    Returns
    -------
    out : object like :py:class:`.OrderParameter`
        An object representing the orderparameter.
    """
    factory_map = {
        'orderparameter': {'cls': OrderParameter},
        'orderparameterposition': {'cls': OrderParameterPosition},
        'position': {'cls': OrderParameterPosition},
        'orderparameterdistance': {'cls': OrderParameterDistance},
        'distance': {'cls': OrderParameterDistance},
        'orderparameterangle': {'cls': OrderParameterAngle},
        'angle': {'cls': OrderParameterAngle},
        'dihedral': {'cls': OrderParameterDihedral},
        'orderparameterdihedral': {'cls': OrderParameterDihedral},
    }
    return generic_factory(settings, factory_map, name='orderparameter')
