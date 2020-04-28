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
TS21
"""
def test_changePSV_RR(qtbot):
    '''
    Test the change of the RR
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    print(esp32)

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_start_vent, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.toolbar

    # Enter the menu and the PSV Settings tab
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings

    # Try to increase the value
    startingValue = window.settings._all_spinboxes['respiratory_rate'].value()

    i = startingValue
    oldValue = 0
    while i <= int(config['respiratory_rate']['max'] + 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('respiratory_rate', i)
        oldValue = i
        i = i + int(config['respiratory_rate']['step'])
        assert window.settings._all_spinboxes['respiratory_rate'].value() <= config['respiratory_rate']['max']

    # Try to decrease the value
    window._start_stop_worker._settings.update_spinbox_value('respiratory_rate', startingValue)

    i = startingValue
    oldValue = 0
    while i >= int(config['respiratory_rate']['min'] - 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('respiratory_rate', i)
        oldValue = i
        i = i - int(config['respiratory_rate']['step'])
        assert window.settings._all_spinboxes['respiratory_rate'].value() >= config['respiratory_rate']['min']


"""
TS22
"""
def test_changePSV_PINSP(qtbot):
    '''
    Test the change of the Pinsp
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    print(esp32)

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_start_vent, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.toolbar

    # Enter the menu and the PSV Settings tab
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings

    # Try to increase the value
    startingValue = window.settings._all_spinboxes['insp_pressure'].value()

    i = startingValue
    oldValue = 0
    while i <= int(config['insp_pressure']['max'] + 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('insp_pressure', i)
        oldValue = i
        i = i + int(config['insp_pressure']['step'])
        assert window.settings._all_spinboxes['insp_pressure'].value() <= config['insp_pressure']['max']

    # Try to decrease the value
    window._start_stop_worker._settings.update_spinbox_value('insp_pressure', startingValue)

    i = startingValue
    oldValue = 0
    while i >= int(config['insp_pressure']['min'] - 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('insp_pressure', i)
        oldValue = i
        i = i - int(config['insp_pressure']['step'])
        assert window.settings._all_spinboxes['insp_pressure'].value() >= config['insp_pressure']['min']


"""
TS26
"""
def test_changePSV_RR_presets(qtbot):
    '''
    Test the change of the RR
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    print(esp32)

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_start_vent, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.toolbar

    # Enter the menu and the PSV Settings tab
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings

    qtbot.mouseClick(window.settings.fake_btn_rr, QtCore.Qt.LeftButton)
    assert window.settings._current_preset.isVisible()


"""
TS27
"""
def test_changePSV_RR_presets(qtbot):
    '''
    Test the change of the RR and load the presets
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    print(esp32)

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_start_vent, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.toolbar

    # Enter the menu and the PSV Settings tab
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings

    # Try to increase the value
    startingValue = window.settings._all_spinboxes['respiratory_rate'].value()
    window._start_stop_worker._settings.update_spinbox_value('respiratory_rate', startingValue+1)

    assert window.settings._all_spinboxes['respiratory_rate'].value() != startingValue

    # Load the presets
    qtbot.mouseClick(window.settings._button_loadpreset, QtCore.Qt.LeftButton)
    assert window.settings._all_spinboxes['respiratory_rate'].value() == startingValue
