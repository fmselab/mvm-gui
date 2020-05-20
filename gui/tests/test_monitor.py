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

    # Go Back
    qtbot.mouseClick(window.button_backalarms, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu


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
    assert window.data_filler._frozen == True
    assert window.rightbar.currentWidget() == window.frozen_right
    assert window.bottombar.currentWidget() == window.frozen_bot

    # Unfreeze plots
    qtbot.mouseClick(window.button_unfreeze, QtCore.Qt.LeftButton)
    assert window.data_filler._frozen == False


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

    assert window.monitors['o2'].label_name == "FiO<sub>2</sub>"


"""
TH16
"""
def check_RR_on_monitor(qtbot):
    '''
    Check that the RR monitor has been initialized
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    assert window.monitors['bpm'].label_name == "Meas. RR"


"""
TH17
"""
def check_MaxPInsp_on_monitor(qtbot):
    '''
    Check that the Max(P(insp)) monitor has been initialized
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    assert window.monitors['peak'].label_name == "Max P<sub>insp</sub>"


"""
TH18
"""
def check_VTidal_on_monitor(qtbot):
    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    assert window.monitors['total_inspired_volume'].label_name == "V<sub>tidal</sub>"


"""
TH19
"""
def check_Battery_on_monitor(qtbot):
    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    assert window.monitors['battery_charge'].label_name == "Battery [%]"


"""
TH20
"""
def check_PowerSource_on_monitor(qtbot):
    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    assert window.monitors['battery_powered'].label_name == "Power Source"


"""
TH21
"""
def check_Temperature_on_monitor(qtbot):
    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    assert window.monitors['temperature'].label_name == "Temperature"


"""
TH22
"""
def check_plots_on_monitor(qtbot):
    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    assert window.plots['plot_top'].name == "PAW"
    assert window.plots['plot_mid'].name == "V<sub>tidal</sub>"
    assert window.plots['plot_bot'].name == "Flow"


"""
TS32-TS45
"""
@pytest.mark.parametrize("code, expected, message, monitorName,overMax", [(8,1 << 8, "Pressure to patient mouth too low", "pressure_patient_mouth", False),
                                                     (9,1 << 9, "Pressure to patient mouth too high", "pressure_patient_mouth", True),
                                                     (10,1 << 10, "Inpiratory flux too low", "insp_flux", False),
                                                     (11,1 << 11, "Inpiratory flux too high", "insp_flux", True),
                                                     (12,1 << 12, "Expiratory flux too low", "expr_flux", False),
                                                     (13,1 << 13, "Expiratory flux too high", "expr_flux", True),
                                                     (14,1 << 14, "Tidal volume too low", "total_inspired_volume", False),
                                                     (15,1 << 15, "Tidal volume too high", "total_inspired_volume", True),
                                                     (16,1 << 16, "O2 too low", "oxygen_concentration", False),
                                                     (17,1 << 17, "O2 too high", "oxygen_concentration", True),
                                                     (18,1 << 18, "PEEP too low", "peep", False),
                                                     (19,1 << 19, "PEEP too high", "peep", True),
                                                     (20,1 << 20, "Respiratory rate too low", "beats_per_minute", False),
                                                     (21,1 << 21, "Respiratory rate too high", "beats_per_minute", True)])
def test_gui_alarm(qtbot, code, expected, message, monitorName,overMax):
    assert qt_api.QApplication.instance() is not None

    if monitorName == "":
        pass
    else:
        esp32 = FakeESP32Serial(config)
        qtbot.addWidget(esp32)

        window = MainWindow(config, esp32)
        window.show()
        qtbot.addWidget(window)
        qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)

        minValue = float(window.monitors[monitorName].label_min.text())
        maxValue = float(window.monitors[monitorName].label_max.text())

        if overMax:
            newValue = maxValue + 1
        else:
            newValue = minValue - 1

        window.monitors[monitorName].update_value(newValue)
        window.monitors[monitorName].set_alarm_state(True)

        # Check the background color of the monitor
        esp32.raise_gui_alarm()
        palette = window.monitors[monitorName].palette()
        role = window.monitors[monitorName].backgroundRole()
        palette.setColor(role, QtGui.QColor(window.monitors[monitorName].alarmcolor))
        assert window.monitors[monitorName].palette() == palette

        # Select the monitor and check if the alarm has been snoozed
        window.monitors[monitorName].update_value(maxValue)
        # Reset the alarm
        window.gui_alarm.clear_alarm(monitorName)
        qtbot.mouseClick(window.monitors[monitorName], QtCore.Qt.LeftButton)

        assert window.monitors[monitorName].palette().color(window.monitors[monitorName].backgroundRole()) == QtGui.QColor("#000000")


"""
TS49
"""
def test_gui_temperatureAlarm(qtbot):
    assert qt_api.QApplication.instance() is not None

    monitorName = "temperature"

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    window.show()
    qtbot.addWidget(window)
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)

    # New out-ranged value

    newValue = 76

    window.monitors[monitorName].update_value(newValue)
    window.monitors[monitorName].set_alarm_state(True)

    # Check the background color of the monitor
    esp32.raise_gui_alarm()
    assert window.monitors[monitorName].palette().color(window.monitors[monitorName].backgroundRole()) == QtGui.QColor(
        "red")


"""
TH23
"""
def check_Ve_on_monitor(qtbot):
    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    assert window.monitors['volume_minute'].label_name == "V<sub>E</sub>"