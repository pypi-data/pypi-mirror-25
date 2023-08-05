#!/usr/bin/env python3

# system modules
import warnings

# internal modules
from .temperature import cel2kel,kel2cel
from .constants import stefan_boltzmann_constant

# external modules
import numpy as np

def blackbody_radiation(T):
    r""" 
    Calculate the total emitted radiation for a blackbody surface at a given
    temperature

    Args:
        T (numpy.ndarray): temperature in Kelvin

    Returns:
        numpy.ndarray : the total emitted blackbody radiation
        :math:`\left[I_\mathrm{total}\right] = \frac{W}{m^2}`
    """
    # convert to an array
    kelvin = cel2kel(kel2cel(T))
    oldshape = kelvin.shape
    kelvin = kelvin.reshape(-1)

    rad = stefan_boltzmann_constant * kelvin ** 4

    return rad.reshape(oldshape)


