#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Wrapper to enable lifepo4wered library to Python.
reference: http://lifepo4wered.com/lifepo4wered-pi3.html
"""

from .defines import (ACCESS_READ, ACCESS_WRITE, TOUCH_INACTIVE, TOUCH_START,
    TOUCH_STOP, TOUCH_HELD, TOUCH_ACTIVE_MASK, TOUCH_MASK, LED_STATE_OFF,
    LED_STATE_ON, LED_STATE_PULSING, LED_STATE_FLASHING, AUTO_BOOT_OFF,
    AUTO_BOOT_VBAT, AUTO_BOOT_VBAT_SMART, AUTO_BOOT_VIN, AUTO_BOOT_VIN_SMART)
from .variablesEnum import variablesEnum
from .functions import canRead, canWrite, read, write

__author__ = "Frederick Lussier <frederick.lussier@hotmail.com>"
__status__ = "dev"
__version__ = "0.1.1"
__date__ = "september 20th 2017"

__ALL__ = [
    "ACCESS_READ", "ACCESS_WRITE", "TOUCH_INACTIVE", "TOUCH_START",
    "TOUCH_STOP", "TOUCH_HELD", "TOUCH_ACTIVE_MASK", "TOUCH_MASK", 
    "LED_STATE_OFF", "LED_STATE_ON", "LED_STATE_PULSING",
    "LED_STATE_FLASHING", "AUTO_BOOT_OFF", "AUTO_BOOT_VBAT",
    "AUTO_BOOT_VBAT_SMART", "AUTO_BOOT_VIN", "AUTO_BOOT_VIN_SMART",
    "variablesEnum", 
    "canRead", 
    "canWrite", 
    "read", 
    "write"]