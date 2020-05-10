#!/usr/bin/env python3
'''
This module implements the spirometer calibration procedure, guiding the
user through it.
'''

import os
from PyQt5 import QtWidgets, uic
from calibration.regression_tools import data_regression

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
        uifile = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "spirometer.ui")

        uic.loadUi(uifile, self)

        self._esp32 = None
        self._mainwindow = None
        self._coefficients = []

        self.retry_button.setEnabled(False)
        self.retry_button.clicked.connect(self._start_calibration)
        self.start_calibration.clicked.connect(self._start_calibration)
        self.back_button.clicked.connect(self._accept_values)

    def connect_mainwindow_esp32(self, mainwindow, esp32):
        """
        Connect the ESP32Serial istance.
        """

        self._esp32 = esp32
        self._mainwindow = mainwindow

    def _accept_values(self):
        """
        Send coefficients to ESP32 and quit the procedure
        """

        if self._coefficients != []:
            for index in range(5):
                self._esp32.set("venturi_coefficient_%d" % index,
                                self._coefficients[index])

        self._mainwindow.goto_new_patient()

    def _start_calibration(self):
        """
        Start retrieving data to fit.
        """

        self.start_calibration.setEnabled(False)
        self.back_button.setEnabled(False)
        self.retry_button.setEnabled(False)
        self.completion_bar.setValue(0)
        self._coefficients = []
        self.endstatus_label.setText("")

        try:
            calibrator = self._esp32.venturi_calibration()

            flows = []
            delta_ps = []
            for completion, flow, delta_p in calibrator.data():
                self.completion_bar.setValue(completion)
                flows.append(flow)
                delta_ps.append(delta_p)

            self._coefficients, chi_sq, ndf = data_regression(delta_ps, flows)
            print('Fit coefficients', self._coefficients)
            if self._coefficients == []:
                raise Exception("invalid data points")
            if chi_sq/ndf > 10:
                raise Exception("Fit has a chi 2 too large")
            self.endstatus_label.setText("Success")
        except: #pylint: disable=W0702
            self.start_calibration.setEnabled(True)
            self.retry_button.setEnabled(True)
            self.endstatus_label.setText("Venturi spirometer\npressure probes inverted")
        finally:
            self.back_button.setEnabled(True)
            del calibrator
