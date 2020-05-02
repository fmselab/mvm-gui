#!/usr/bin/env python3
'''
This module implements the spirometer calibration procedure, guiding the
user through it.
'''

import os
from PyQt5 import QtWidgets, uic


class SpirometerCalibration(QtWidgets.QWidget):
    '''
    SpirometerCalibration widget. User guidance through the procedure and
    calculations.
    '''
    def __init__(self, *args):
        """
        Constructor. Initializes the SpirometerCalibration widget.
        """

        super(SpirometerCalibration, self).__init__(*args)
        uifile = os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            "spirometer.ui")

        uic.loadUi(uifile, self)
        self._esp32 = None

    def connect_esp32(self, esp32):
        """
        Connect the ESP32Serial istance.
        """

        self._esp32 = esp32
