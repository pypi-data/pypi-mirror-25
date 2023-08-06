#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
reference: lifepo4wered-data.h
"""

from . import defines
from .variablesEnum import variablesEnum
from . import lifepo4weredSO

def canRead(variable):
    """
    mention if an element can be read.

    :param variable: the element to evaluate.
    :type variable: Lifepo4weredEnum
    :return: true when read access is available, otherwise false.
    :rtype: bool
    :raises ValueError: if parameter value is not a member of Lifepo4weredEnum.
    """
    if variable not in variablesEnum:
        raise ValueError('Use a lifepo4wered enum element as parameter.')

    return lifepo4weredSO.access_lifepo4wered(variable.value, defines.ACCESS_READ)

def canWrite(variable):
    """
    mention if an element can be written.

    :param variable: the element to evaluate.
    :type variable: Lifepo4weredEnum
    :return: true when write access is available, otherwise false
    :rtype: bool
    :raises ValueError: if parameter value is not a member of Lifepo4weredEnum
    """
    if variable not in variablesEnum:
        raise ValueError('Use a lifepo4wered enum element as parameter.')

    return lifepo4weredSO.access_lifepo4wered(variable.value, defines.ACCESS_WRITE)

def read(variable):
    """
    read an element from LiFePO4wered.

    :param variable: the element to read.
    :type variable: Lifepo4weredEnum
    :return: the value of the element
    :rtype: int
    :raises ValueError: if parameter value is not a member of Lifepo4weredEnum
    """
    if variable not in variablesEnum:
        raise ValueError('Use a lifepo4wered enum element as read parameter.')
    
    if canRead(variable):
        return lifepo4weredSO.read_lifepo4wered(variable.value)
    else:
        raise RuntimeError('You cannot read {0} value, just write it'.format(variable.name))

def write(variable, value):
    """
    write an element to LiFePO4wered.

    :param variable: the element.
    :type variable: Lifepo4weredEnum
    :param int value: the value to write.
    :return: the written value
    :rtype: int
    :raises ValueError: if variable parameter is not a member of Lifepo4weredEnum
    :raises ValueError: if value is not an int type
    """
    if variable not in variablesEnum:
        raise ValueError('Use a lifepo4wered enum element as write element.')
    
    if isinstance(value, int) is False:
        raise TypeError('Use a int as value.')

    if canWrite(variable):
        return lifepo4weredSO.write_lifepo4wered(variable.value, value)
    else:
        raise RuntimeError('You cannot write {0} value, just read it'.format(variable.name))
