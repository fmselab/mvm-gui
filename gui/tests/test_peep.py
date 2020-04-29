#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
from communication.peep import PEEP
from mainwindow import MainWindow
from communication.fake_esp32serial import FakeESP32Serial


"""
TH13
"""
def check_peep_on_monitor(qtbot):
    '''
    Check that the peep monitor has been initialized
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    assert window.monitors['peep'] is not None
