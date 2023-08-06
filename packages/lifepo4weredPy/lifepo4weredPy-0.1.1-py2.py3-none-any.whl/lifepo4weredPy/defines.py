#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
reference: lifepo4wered-data.h
"""

# Register access masks
ACCESS_READ = 0x01
ACCESS_WRITE = 0x02

# Touch states
TOUCH_INACTIVE = 0x00
TOUCH_START = 0x03
TOUCH_STOP = 0x0C
TOUCH_HELD = 0x0F

# Touch masks
TOUCH_ACTIVE_MASK = 0x03
TOUCH_MASK  = 0x0F

# LED states when Pi on
LED_STATE_OFF = 0x00
LED_STATE_ON = 0x01
LED_STATE_PULSING = 0x02
LED_STATE_FLASHING = 0x03

# Auto boot settings
AUTO_BOOT_OFF = 0x00
AUTO_BOOT_VBAT = 0x01
AUTO_BOOT_VBAT_SMART = 0x02
AUTO_BOOT_VIN = 0x03
AUTO_BOOT_VIN_SMART = 0x04