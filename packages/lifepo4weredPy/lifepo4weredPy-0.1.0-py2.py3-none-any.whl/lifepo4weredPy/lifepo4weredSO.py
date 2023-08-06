#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
reference: lifepo4wered-data.h
"""

import ctypes 
import os.path

try:
    lib = ctypes.CDLL('liblifepo4wered.so')
    # this file should be found in the runtime paths.
    #  At least, use the LD_LIBRARY_PATH export path to set the path of the so file.
    #  echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/your/custom/path/" >> ~/.bashrc
except:
    #For testing purpose, otherwise the import mechanism
    # return an error. Anyway it is mocked during test.
    lib = None

def access_lifepo4wered(eLiFePO4weredVar, access_mask):
    """
    Determine if the specified variable can be accessed in the 
    specified manner (read, write or both)
    """
    return lib.access_lifepo4wered(eLiFePO4weredVar, access_mask)

def read_lifepo4wered(eLiFePO4weredVar):
    """
    Read data from LiFePO4wered/Pi
    """
    return lib.read_lifepo4wered(eLiFePO4weredVar)

def write_lifepo4wered(eLiFePO4weredVar, value):
    """
    Write data to LiFePO4wered/Pi
    """
    return lib.write_lifepo4wered(eLiFePO4weredVar, value)
