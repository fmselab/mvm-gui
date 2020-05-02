#!/usr/bin/env python3
'''
This module implements the spirometer calibration procedure, guiding the
user through it.
'''

import os
from PyQt5 import QtWidgets, uic
import numpy as np


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

        for index in range(5):
            self._esp32.set("venturi_coefficient_%d" % index,
                            self._coefficients[index])

            self._mainwindow.show_startup()

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

            # TODO call the function to do the regression
            self._coefficients, chi_sq, p_value = self._data_regression(flows, delta_ps)
            if self._coefficients == []:
                raise Exception("invalid data points")
            if p_value < 0.5:
                raise Exception("Fit has a p_value too low")
            self.endstatus_label.setText("Succeeded")
        except: #pylint: disable=W0702
            self.start_calibration.setEnabled(True)
            self.retry_button.setEnabled(True)
            self.endstatus_label.setText("Failed")
        finally:
            self.back_button.setEnabled(True)
            del calibrator

    def _check_data(x, y, cov_th=10):
        '''
        Checks if the data has a covariance 
        bigger than cov_th, and returns the 
        data split in x and y
        
        arguments:
        - x: a list with the data x values
        - y: a list with the data y values
        - cov_th: threshold to use for the covariance
        
        returns:
        a list with data x and y if the covariance
        condition is satisfied, else it returns 
        an empty list
        '''
        
        cov = np.cov(x,y)
        
        if np.abs(cov[1,1]) > cov_th and np.abs(cov[0,1]) > cov_th:
            return [x, y]    

        return []

    def _data_regression(x, y, deg=4, full=True):
        '''
        Performs the data regression with a 
        polynomial of order deg.
        
        arguments:
        - x: a list with the data x values
        - y: a list with the data y values
        - deg: the order of the polynomial
        
        returns:
        - a list with the plynomial coefficients
        - the chi squared
        - the p-value
        '''

        data = self._check_data(x, y)

        if data:
            coeff = np.polyfit(x, y, deg=deg)
            chi_squared = np.sum((np.polyval(coeff, x) - y) ** 2)
            p_value = 1 - stats.chi2.cdf(chi_squared, len(x)-deg)

            if full: return np.flip(coeff), chi_squared, p_value
            else:    return np.flip(coeff)
        else:
            return []
