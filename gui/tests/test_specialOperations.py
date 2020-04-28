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
TS24
"""
def test_expiratoryPause(qtbot):
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

    # Enter the menu and the Special Operations section
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_specialops, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.specialbar

    # Click on the Expiratory Pause button
    qtbot.mouseClick(window.specialbar.button_expause, QtCore.Qt.LeftButton)
    qtbot.waitUntil(lambda: not window.specialbar._timer['pause_exhale'].isActive(), timeout=10000)


"""
TS25
"""
def test_inspiratoryPause(qtbot):
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

    # Enter the menu and the Special Operations section
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_specialops, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.specialbar

    # Click on the Inspiratory Pause button
    qtbot.mouseClick(window.specialbar.button_inspause, QtCore.Qt.LeftButton)
    qtbot.waitUntil(lambda: not window.specialbar._timer['pause_inhale'].isActive(), timeout=10000)

