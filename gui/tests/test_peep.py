#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
from communication.peep import peep
from mainwindow import MainWindow
from communication.fake_esp32serial import FakeESP32Serial

"""
TH11
"""
def test_peepReset(qtbot):
    '''
    Test the reset of the Peep
    '''

    p = PEEP()

    # Set a negative value for the t5 parameter, so the time t is obiously greater than t5
    t5 = p.t5
    p.t5 = -1
    t0 = p.t0

    # Force the flow
    p.flow()

    assert p.t0 != t0

    p.t5 = t5


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
