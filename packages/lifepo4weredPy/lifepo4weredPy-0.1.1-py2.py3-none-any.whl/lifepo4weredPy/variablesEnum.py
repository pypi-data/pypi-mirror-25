#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
reference: lifepo4wered-data.h
"""

from enum import Enum, unique

@unique
class variablesEnum(Enum):
    I2C_REG_VER = 0
    I2C_ADDRESS = 1
    LED_STATE = 2
    TOUCH_STATE = 3
    TOUCH_CAP_CYCLES = 4
    TOUCH_THRESHOLD = 5
    TOUCH_HYSTERESIS = 6
    DCO_RSEL = 7
    DCO_DCOMOD = 8
    VIN = 9
    VBAT = 10
    VOUT = 11
    VBAT_MIN = 12 
    VBAT_SHDN = 13
    VBAT_BOOT = 14
    VOUT_MAX = 15
    VIN_THRESHOLD = 16
    VOFFSET_ADC = 17
    AUTO_BOOT = 18
    WAKE_TIME = 19
    SHDN_DELAY = 20
    AUTO_SHDN_TIME = 21
    PI_RUNNING = 22
    CFG_WRITE = 23