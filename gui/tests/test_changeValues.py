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
TS21
"""
def test_changePSV_RR_2(qtbot):
    '''
    Test the change of the RR
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

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


"""
TS50
"""
def test_changePRM(qtbot):
    '''
    Test the change of the Pressure for Lung Recruitment
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_start_vent, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.toolbar

    # Enter the menu and the Mode Settings tab
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings

    # Try to increase the value
    startingValue = window.settings._all_spinboxes['lung_recruit_pres'].value()

    i = startingValue
    oldValue = 0
    while i <= int(config['lung_recruit_pres']['max'] + 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('lung_recruit_pres', i)
        oldValue = i
        i = i + int(config['lung_recruit_pres']['step'])
        assert window.settings._all_spinboxes['lung_recruit_pres'].value() <= config['lung_recruit_pres']['max']

    # Try to decrease the value
    window._start_stop_worker._settings.update_spinbox_value('lung_recruit_pres', startingValue)

    i = startingValue
    oldValue = 0
    while i >= int(config['lung_recruit_pres']['min'] - 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('lung_recruit_pres', i)
        oldValue = i
        i = i - int(config['lung_recruit_pres']['step'])
        assert window.settings._all_spinboxes['lung_recruit_pres'].value() >= config['lung_recruit_pres']['min']


"""
TS51
"""
def test_changeTRM(qtbot):
    '''
    Test the change of the Time for Lung Recruitment
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_start_vent, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.toolbar

    # Enter the menu and the Mode Settings tab
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings

    # Try to increase the value
    startingValue = window.settings._all_spinboxes['lung_recruit_time'].value()

    i = startingValue
    oldValue = 0
    while i <= int(config['lung_recruit_time']['max'] + 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('lung_recruit_time', i)
        oldValue = i
        i = i + int(config['lung_recruit_time']['step'])
        assert window.settings._all_spinboxes['lung_recruit_time'].value() <= config['lung_recruit_time']['max']

    # Try to decrease the value
    window._start_stop_worker._settings.update_spinbox_value('lung_recruit_time', startingValue)

    i = startingValue
    oldValue = 0
    while i >= int(config['lung_recruit_time']['min'] - 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('lung_recruit_time', i)
        oldValue = i
        i = i - int(config['lung_recruit_time']['step'])
        assert window.settings._all_spinboxes['lung_recruit_time'].value() >= config['lung_recruit_time']['min']


"""
TS52
"""
def test_change_ETS(qtbot):
    '''
    Test the change of the ETS Parameter

    At the current situation, the test cannot be executed, since the ETS parameter is not loaded from the default values
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_start_vent, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.toolbar

    # Enter the menu and the Mode Settings tab
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings

    # Try to increase the value
    startingValue = window.settings._all_spinboxes['flow_trigger'].value()

    i = startingValue
    oldValue = 0
    while i <= int(config['flow_trigger']['max'] + 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('flow_trigger', i)
        oldValue = i
        i = i + int(config['flow_trigger']['step'])
        assert window.settings._all_spinboxes['flow_trigger'].value() <= config['flow_trigger']['max']

    # Try to decrease the value
    window._start_stop_worker._settings.update_spinbox_value('flow_trigger', startingValue)

    i = startingValue
    oldValue = 0
    while i >= int(config['flow_trigger']['min'] - 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('flow_trigger', i)
        oldValue = i
        i = i - int(config['flow_trigger']['step'])
        assert window.settings._all_spinboxes['flow_trigger'].value() >= config['flow_trigger']['min']


"""
TS58
"""
def test_change_ITS_PSV(qtbot):
    '''
    Test the change of the ITS Parameter

    At the current situation, the test cannot be executed, since the ITS parameter is not loaded from the default values
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_start_vent, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.toolbar

    # Enter the menu and the Mode Settings tab
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings

    # Try to increase the value
    startingValue = window.settings._all_spinboxes['pressure_trigger'].value()

    i = startingValue
    oldValue = 0
    while i <= int(config['pressure_trigger']['max'] + 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('pressure_trigger', i)
        oldValue = i
        i = i + int(config['pressure_trigger']['step'])
        assert window.settings._all_spinboxes['pressure_trigger'].value() <= config['pressure_trigger']['max']

    # Try to decrease the value
    window._start_stop_worker._settings.update_spinbox_value('pressure_trigger', startingValue)

    i = startingValue
    oldValue = 0
    while i >= int(config['pressure_trigger']['min'] - 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('pressure_trigger', i)
        oldValue = i
        i = i - int(config['pressure_trigger']['step'])
        assert window.settings._all_spinboxes['pressure_trigger'].value() >= config['pressure_trigger']['min']


"""
TS59
"""
def test_change_ITS_PCV(qtbot):
    '''
    Test the change of the ITS Parameter

    At the current situation, the test cannot be executed, since the ITS parameter is not loaded from the default values
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_start_vent, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.toolbar

    # Enter the menu and the Mode Settings tab
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings

    # Try to increase the value
    startingValue = window.settings._all_spinboxes['pcv_trigger_pressure'].value()

    i = startingValue
    oldValue = 0
    while i <= int(config['pcv_trigger_pressure']['max'] + 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('pcv_trigger_pressure', i)
        oldValue = i
        i = i + int(config['pcv_trigger_pressure']['step'])
        assert window.settings._all_spinboxes['pcv_trigger_pressure'].value() <= config['pcv_trigger_pressure']['max']

    # Try to decrease the value
    window._start_stop_worker._settings.update_spinbox_value('pcv_trigger_pressure', startingValue)

    i = startingValue
    oldValue = 0
    while i >= int(config['pcv_trigger_pressure']['min'] - 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('pcv_trigger_pressure', i)
        oldValue = i
        i = i - int(config['pcv_trigger_pressure']['step'])
        assert window.settings._all_spinboxes['pcv_trigger_pressure'].value() >= config['pcv_trigger_pressure']['min']


"""
TS60
"""
def test_change_apenea_rr(qtbot):

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_start_vent, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.toolbar

    # Enter the menu and the Mode Settings tab
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings

    # Try to increase the value
    startingValue = window.settings._all_spinboxes['apnea_rr'].value()

    i = startingValue
    oldValue = 0
    while i <= int(config['apnea_rr']['max'] + 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('apnea_rr', i)
        oldValue = i
        i = i + int(config['apnea_rr']['step'])
        assert window.settings._all_spinboxes['apnea_rr'].value() <= config['apnea_rr']['max']

    # Try to decrease the value
    window._start_stop_worker._settings.update_spinbox_value('apnea_rr', startingValue)

    i = startingValue
    oldValue = 0
    while i >= int(config['apnea_rr']['min'] - 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('apnea_rr', i)
        oldValue = i
        i = i - int(config['apnea_rr']['step'])
        assert window.settings._all_spinboxes['apnea_rr'].value() >= config['apnea_rr']['min']


"""
TS61
"""
def test_change_apenea_pinsp(qtbot):

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_start_vent, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.toolbar

    # Enter the menu and the Mode Settings tab
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings

    # Try to increase the value
    startingValue = window.settings._all_spinboxes['apnea_insp_press'].value()

    i = startingValue
    oldValue = 0
    while i <= int(config['apnea_insp_press']['max'] + 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('apnea_insp_press', i)
        oldValue = i
        i = i + int(config['apnea_insp_press']['step'])
        assert window.settings._all_spinboxes['apnea_insp_press'].value() <= config['apnea_insp_press']['max']

    # Try to decrease the value
    window._start_stop_worker._settings.update_spinbox_value('apnea_insp_press', startingValue)

    i = startingValue
    oldValue = 0
    while i >= int(config['apnea_insp_press']['min'] - 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('apnea_insp_press', i)
        oldValue = i
        i = i - int(config['apnea_insp_press']['step'])
        assert window.settings._all_spinboxes['apnea_insp_press'].value() >= config['apnea_insp_press']['min']


"""
TS53
"""
def test_change_ApneaLag(qtbot):
    '''
    Test the change of the Apnea Lag Parameter
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_start_vent, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.toolbar

    # Enter the menu and the Mode Settings tab
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings

    # Try to increase the value
    startingValue = window.settings._all_spinboxes['max_apnea_time'].value()

    i = startingValue
    oldValue = 0
    while i <= int(config['max_apnea_time']['max'] + 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('max_apnea_time', i)
        oldValue = i
        i = i + int(config['max_apnea_time']['step'])
        assert window.settings._all_spinboxes['max_apnea_time'].value() <= config['max_apnea_time']['max']

    # Try to decrease the value
    window._start_stop_worker._settings.update_spinbox_value('max_apnea_time', startingValue)

    i = startingValue
    oldValue = 0
    while i >= int(config['max_apnea_time']['min'] - 1) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('max_apnea_time', i)
        oldValue = i
        i = i - int(config['max_apnea_time']['step'])
        assert window.settings._all_spinboxes['max_apnea_time'].value() >= config['max_apnea_time']['min']


"""
TS54
"""
def test_changePCV_IE(qtbot):
    '''
    Test the change of the I:E
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

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
    startingValue = window.settings._all_spinboxes['insp_expir_ratio'].value()

    i = startingValue
    oldValue = 0
    while i <= float(config['insp_expir_ratio']['max'] + float(config['insp_expir_ratio']['step'])) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('insp_expir_ratio', i)
        oldValue = i
        i = i + float(config['insp_expir_ratio']['step'])
        assert window.settings._all_spinboxes['insp_expir_ratio'].value() <= config['insp_expir_ratio']['max']

    # Try to decrease the value
    window._start_stop_worker._settings.update_spinbox_value('insp_expir_ratio', startingValue)

    i = startingValue
    oldValue = 0
    while i >= float(config['insp_expir_ratio']['min'] - float(config['insp_expir_ratio']['step'])) or i == oldValue:
        window._start_stop_worker._settings.update_spinbox_value('insp_expir_ratio', i)
        oldValue = i
        i = i - float(config['insp_expir_ratio']['step'])
        assert window.settings._all_spinboxes['insp_expir_ratio'].value() >= config['insp_expir_ratio']['min']