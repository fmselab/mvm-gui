#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from .mvm_basics import *
from mainwindow import MainWindow
from messagebox import MessageBox
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

    # Go back
    qtbot.mouseClick(window.settings._button_close, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.main

"""
TH26
"""
def test_settingsWhileStarting(qtbot):
    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    assert window.button_start_settings.isEnabled() == False

    # Open the settings page
    qtbot.mouseClick(window.button_start_settings, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.settings


"""
TS48
"""
def test_from_PSV_to_PCV(qtbot):
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

    assert "Stopped" in window._start_stop_worker._toolbar.label_status.text() and "PCV" in window._start_stop_worker._toolbar.label_status.text()

    # Enter the menu and change to PSV
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_autoassist, QtCore.Qt.LeftButton)

    assert window.bottombar.currentWidget() == window.messagebar

    qtbot.waitUntil(
        lambda: "Stopped" in window._start_stop_worker._toolbar.label_status.text() and "PSV" in window._start_stop_worker._toolbar.label_status.text(),
        timeout=3000)

    # Change to PCV
    qtbot.mouseClick(window.button_autoassist, QtCore.Qt.LeftButton)

    qtbot.waitUntil(
        lambda: "Stopped" in window._start_stop_worker._toolbar.label_status.text() and "PCV" in window._start_stop_worker._toolbar.label_status.text(),
        timeout=3000)


"""
TH29
"""
def test_MessageBox_Warning(qtbot):
    msg = MessageBox()

    def foo():
        pass

    callbacks = {msg.Ok: foo}

    msg.warning("CHANGE OF MODE",
                "The ventilator changed from PSV to PCV mode.",
                "The microcontroller raised the backup flag.",
                "",
                callbacks,
                True)

    assert msg is not None


"""
TH30
"""
def test_MessageBox_Critical(qtbot):
    msg = MessageBox()

    def foo():
        pass

    callbacks = {msg.Ok: foo}

    msg.critical("CHANGE OF MODE",
                "The ventilator changed from PSV to PCV mode.",
                "The microcontroller raised the backup flag.",
                "",
                callbacks,
                True)

    assert msg is not None


"""
TH31
"""
def test_MessageBox_Question(qtbot):
    msg = MessageBox()

    def foo():
        pass

    callbacks = {msg.Ok: foo}

    msg.question("CHANGE OF MODE",
                "The ventilator changed from PSV to PCV mode.",
                "The microcontroller raised the backup flag.",
                "",
                callbacks,
                True)

    assert msg is not None


"""
TS57
"""
def test_change_Mode_while_running(qtbot):

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

    assert "Stopped" in window._start_stop_worker._toolbar.label_status.text() and "PCV" in window._start_stop_worker._toolbar.label_status.text()

    # Enter the menu and start
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_startstop, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.messagebar.button_confirm, QtCore.Qt.LeftButton)

    qtbot.waitUntil(
        lambda: "Running" in window._start_stop_worker._toolbar.label_status.text() and "PCV" in window._start_stop_worker._toolbar.label_status.text(),
        timeout=3000)

    assert window.button_autoassist.isEnabled() == True