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
TS14
"""
def test_start_operating(qtbot):
    '''
    Test the start of the PCV Mode
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

    assert "Stopped" in window._start_stop_worker._toolbar.label_status.text() and "PCV" in window._start_stop_worker._toolbar.label_status.text()

    # Enter the menu and start
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_startstop, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.messagebar.button_confirm, QtCore.Qt.LeftButton)

    qtbot.waitUntil(
        lambda: "Running" in window._start_stop_worker._toolbar.label_status.text() and "PCV" in window._start_stop_worker._toolbar.label_status.text(),
        timeout=3000)
    assert window.button_autoassist.isEnabled() == False

    assert window._start_stop_worker.is_running()

    qtbot.waitUntil(
        lambda: window.button_startstop.isEnabled(), timeout=5000)

    # Enter the menu and stop the working
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_startstop, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.messagebar.button_confirm, QtCore.Qt.LeftButton)
    qtbot.waitUntil(
        lambda: "Stopped" in window._start_stop_worker._toolbar.label_status.text() and "PCV" in window._start_stop_worker._toolbar.label_status.text(),
        timeout=3000)


"""
TS20
"""
def test_start_operating_PSV(qtbot):
    '''
    Test the start of the PSV Mode
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

    assert "Stopped" in window._start_stop_worker._toolbar.label_status.text() and "PCV" in window._start_stop_worker._toolbar.label_status.text()

    # Enter the menu and start
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_autoassist, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_startstop, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.messagebar.button_confirm, QtCore.Qt.LeftButton)

    qtbot.waitUntil(
        lambda: "Running" in window._start_stop_worker._toolbar.label_status.text() and "PSV" in window._start_stop_worker._toolbar.label_status.text(),
        timeout=3000)
    assert window.button_autoassist.isEnabled() == False

    assert window._start_stop_worker.is_running()


"""
TS27
"""
def test_changeMode(qtbot):
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

    assert "Stopped" in window._start_stop_worker._toolbar.label_status.text() and "PCV" in window._start_stop_worker._toolbar.label_status.text()

    # Enter the menu and change the mode, without starting the ventilator
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_autoassist, QtCore.Qt.LeftButton)

    assert "Stopped" in window._start_stop_worker._toolbar.label_status.text() and "PSV" in window._start_stop_worker._toolbar.label_status.text()


"""
TS28
"""
def test_wrongConfigurationFile(qtbot):
    try:
        assert qt_api.QApplication.instance() is not None

        wrongConfigurationFile()

        esp32 = FakeESP32Serial(config)
        qtbot.addWidget(esp32)
    except FileNotFoundError:
        pass
    except:
        assert False


"""
TH11
"""
def test_settingsWileRunning(qtbot):
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

    assert "Stopped" in window._start_stop_worker._toolbar.label_status.text() and "PCV" in window._start_stop_worker._toolbar.label_status.text()

    # Enter the menu and start
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_startstop, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.messagebar.button_confirm, QtCore.Qt.LeftButton)
    qtbot.waitUntil(lambda: "Running" in window._start_stop_worker._toolbar.label_status.text() and "PCV" in window._start_stop_worker._toolbar.label_status.text(), timeout=3000)
    assert window.button_autoassist.isEnabled() == False
    assert window._start_stop_worker.is_running()

    # Enter the settins menu
    window._start_stop_worker._init_settings_panel()
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_settingsfork, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.settingsfork
    qtbot.mouseClick(window.button_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings