#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from .mvm_basics import *
from mainwindow import MainWindow
from numpad.numpad import NumPad
from PyQt5.QtCore import QCoreApplication

"""
TH01 
"""
def test_createNumPad(qtbot):
    '''
    Test the creation of the NumPad instance
    '''

    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    pad = NumPad(window)

    assert pad is not None

    time.sleep(0.5)


def checkCode():
    print("Ok")
    assert True


"""
TH02 
"""
def test_codeNumPad(qtbot):
    '''
    Test the assignment and the comparison of the code
    '''

    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    pad = NumPad(window)
    pad.assign_code("1234", checkCode)
    assert pad.func is not None

    # Check that the code is correctly set
    assert pad.code == [1,2,3,4]

    # Try to set the code
    pad.input_number(1)
    pad.input_number(2)
    pad.input_number(3)
    pad.input_number(4)

    pad.check_code()
    assert pad.code == [1, 2, 3, 4]

    time.sleep(0.5)


"""
TS01: Security Requirement - 1 
"""
def test_lockTheScreen(qtbot):
    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    window = MainWindow(config, esp32)
    window.show()
    qtbot.addWidget(window)

    # Click on the menù button
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu

    # Click on the settings button
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsbar

    # Click on the lock screen button
    qtbot.mouseClick(window.button_lockscreen, QtCore.Qt.LeftButton)

    # Check if all the elements in the gui are locked
    assert window.toppane.isEnabled() == False
    assert window.home_button.currentWidget() == window.goto_unlock

    window.close()


"""
TH06
"""
def test_unlockTheScreen(qtbot):
    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    # Click on the menù button
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu

    # Click on the settings button
    qtbot.mouseClick(window.button_start_settings, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsbar

    # Click on the lock screen button
    qtbot.mouseClick(window.button_lockscreen, QtCore.Qt.LeftButton)

    # Check if all the elements in the gui are locked
    assert window.toppane.isEnabled() == False
    assert window.home_button.currentWidget() == window.goto_unlock

    # Unlock the screen
    window.unlock_screen()
    assert window.toppane.isEnabled() == True
    window.close()

