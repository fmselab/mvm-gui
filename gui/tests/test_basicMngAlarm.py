#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
import sys
from .mvm_basics import *
from gui.alarm_handler import AlarmHandler
from mainwindow import MainWindow
from messagebox import MessageBox
from PyQt5.QtCore import QCoreApplication

def test_basics(qtbot):
    '''
    Basic test that works more like a sanity check 
    to ensure we are setting up a QApplication properly
    '''
    assert qt_api.QApplication.instance() is not None

    widget = qt_api.QWidget()
    qtbot.addWidget(widget)
    widget.setWindowTitle("W1")
    widget.show()

    assert widget.isVisible()
    assert widget.windowTitle() == "W1"

"""
TH03 
"""
def test_menu(qtbot):
    '''
    Tests that the menu opens
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
        
    print(esp32)

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu

    window.close()


"""
TS04-TS12
"""
@pytest.mark.parametrize("code, expected, message", [(0, 1, "Gas pressure too low"),
                                                     (1, 2, "Gas pressure too high"),
                                                     (2, 4, "Internal pressure too low (internal leakage)"),
                                                     (3, 8, "Internal pressure too high"),
                                                     (4, 16, "Out of battery power"),
                                                     (5, 32, "Leakage in gas circuit"),
                                                     (6, 64, "Obstruction in idraulic circuit"),
                                                     (7, 128, "Partial obstruction in idraulic circuit"),
                                                     (31, 2147483648, "System failure")])
def test_single_alarm(qtbot, code, expected, message):
    '''
    Tests that when there is an alarm, it is revealed by the get_alarms function
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    messagebox = window.alarm_h._msg_err
    qtbot.addWidget(messagebox)

    code = (1 << code)
    
    esp32.alarms_checkboxes[code].setChecked(True)

    esp32._compute_and_raise_alarms()
    assert esp32.get_alarms().number == expected

    handler = AlarmHandler(config, esp32)
    handler.handle_alarms()

    esp32.reset_alarms()


"""
TS13
"""
def test_not_alarm(qtbot):
    '''
    Tests the absence of alarms
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)

    esp32._compute_and_raise_alarms()
    
    assert esp32.get_alarms().number == 0

    esp32.reset_alarms()


"""
TS15-TS16
"""
@pytest.mark.parametrize("code, expected, message", [(0, 1, ""),
                                                     (1, 2, "")])
def test_single_warning(qtbot, code, expected, message):
    '''
    Tests that when there is a warning, it is revealed by the get_warnings function
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)

    code = (1 << code)

    esp32.warning_checkboxes[code].setChecked(True)

    esp32._compute_and_raise_warnings()
    assert esp32.get_warnings().number == expected

    esp32.reset_warnings()