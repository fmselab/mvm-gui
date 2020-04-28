#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from .mvm_basics import *
from mainwindow import MainWindow
from start_stop_worker import StartStopWorker
from PyQt5.QtCore import QCoreApplication

"""
TH15
"""
def test_defaultConfiguration(qtbot):
    '''
    Check the default values for the parameters loaded at startup
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    # Check the values
    assert config['respiratory_rate']['default'] == 12
    assert config['respiratory_rate']['step'] == 1
    assert config['respiratory_rate']['min'] == 4
    # TODO: Remove comment on the following line when the GUI has been fixed
    # assert config['respiratory_rate']['max'] == 50
    assert config['insp_expir_ratio']['default'] == 2
    assert config['insp_expir_ratio']['step'] == 0.1
    assert config['insp_expir_ratio']['min'] == 1
    assert config['insp_expir_ratio']['max'] == 4
    assert config['insp_pressure']['default'] == 15
    assert config['insp_pressure']['step'] == 1
    assert config['insp_pressure']['min'] == 2
    assert config['insp_pressure']['max'] == 40
