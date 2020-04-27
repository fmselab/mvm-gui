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
    Test the start of the PCV Mode, and then in PSV Mode
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

    work = StartStopWorker(window, config, esp32, window.button_startstop,
            window.button_autoassist, window.toolbar, window.settings)

    assert "Stopped" in work._toolbar.label_status.text() and "PCV" in work._toolbar.label_status.text()

    # Enter the menu and start
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_startstop, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.messagebar.button_confirm, QtCore.Qt.LeftButton)

    qtbot.waitUntil(lambda: "Running" in work._toolbar.label_status.text() and "PCV" in work._toolbar.label_status.text(), timeout=5000)
    assert window.button_autoassist.isEnabled() == False

    # Change the modality
    qtbot.waitUntil(lambda: "Stop" in window.button_startstop.text() and "PCV" in work._toolbar.label_status.text(), timeout=5000)
    qtbot.mouseClick(window.button_startstop, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.messagebar.button_confirm, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.button_autoassist, QtCore.Qt.LeftButton)

    qtbot.stopForInteraction()

    qtbot.waitUntil(lambda: "Stopped" in work._toolbar.label_status.text() and "PSV" in work._toolbar.label_status.text(), timeout=5000)

    # Start the PSV Ventilation
    qtbot.mouseClick(window.button_startstop, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.messagebar.button_confirm, QtCore.Qt.LeftButton)

    qtbot.waitUntil(lambda: "Running" in work._toolbar.label_status.text() and "PSV" in work._toolbar.label_status.text(), timeout=5000)
    assert True

    assert work.is_running()

