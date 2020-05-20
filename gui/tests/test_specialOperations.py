#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
import re
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


"""
TS46
"""
def test_lungRecruitment_1(qtbot):
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

    # Enter the menu and the Special Operations section
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_specialops, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.specialbar

    # Click on the Country Specific Procedures button
    qtbot.mouseClick(window.specialbar.button_lung_recruit, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.specialbar._messagebar.button_confirm, QtCore.Qt.LeftButton)
    qtbot.waitUntil(
        lambda: "Lung Recruitment" in window.specialbar.button_lung_recruit.text(), timeout=3000)


"""
TS47
"""
def test_lungRecruitment_2(qtbot):
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

    # Enter the menu and the Special Operations section
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu
    qtbot.mouseClick(window.button_specialops, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.specialbar

    # Click on the Country Specific Procedures button
    qtbot.mouseClick(window.specialbar.button_lung_recruit, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.specialbar._messagebar.button_confirm, QtCore.Qt.LeftButton)
    qtbot.waitUntil(
        lambda: "Lung Recruitment" in window.specialbar.button_lung_recruit.text(), timeout=3000)
    qtbot.waitUntil(
        lambda: re.search("[0-9]$",window.specialbar.button_lung_recruit.text()) != None, timeout=3000)

    # Stop the procedure
    qtbot.mouseClick(window.specialbar.button_lung_recruit, QtCore.Qt.LeftButton)
    qtbot.waitUntil(
        lambda: "Country" in window.specialbar.button_lung_recruit.text(), timeout=3000)