#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from .mvm_basics import *
from monitor.monitor import Monitor
from mainwindow import MainWindow
from PyQt5.QtCore import QCoreApplication

"""
TH12
"""
def test_monitorSizeMod(qtbot):
    '''
    Test the start of the PCV Mode, and then in PSV Mode
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    monitor = Monitor("Insp. Press.", config)
    qtbot.addWidget(monitor)

    assert monitor.configname == "Insp. Press."

    monitor.handle_resize(None)
    monitor.highlight()
    value = monitor.value
    monitor.update_value(10)

    assert monitor.value == 10
    monitor.value = value


"""
TS17
"""
def test_showAlarmsSettings(qtbot):
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

    # Click on the alarm settings button and reset all the changes
    qtbot.mouseClick(window.button_alarms, QtCore.Qt.LeftButton)
    assert window.centerpane.currentWidget() == window.alarms_settings


"""
TS18
"""
def test_showModeSettings(qtbot):
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

    # Click on the alarm settings button and reset all the changes
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)


"""
TS19
"""
def test_showSpecialOperations(qtbot):
    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    # Click on the menù button
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu

    # Click on the settings button
    qtbot.mouseClick(window.button_specialops, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.specialbar

    # Click on the freeze button
    qtbot.mouseClick(window.button_freeze, QtCore.Qt.LeftButton)
    assert window.rightbar.currentWidget() == window.frozen_right
    assert window.bottombar.currentWidget() == window.frozen_bot

    # Unfreeze the plots
    qtbot.mouseClick(window.button_unfreeze, QtCore.Qt.LeftButton)
    assert window.rightbar.currentWidget() == window.monitors_bar


"""
TH14
"""
def check_FiO2_on_monitor(qtbot):
    '''
    Check that the peep monitor has been initialized
    '''
    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    assert window.monitors['o2'] is not None



