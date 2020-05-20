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
TS55
"""
def test_selftTest_1(qtbot):

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)

    # Open the Self Test section
    qtbot.mouseClick(window.button_start_test, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.self_test

    # Press the Leak check button
    qtbot.mouseClick(window.self_test.btn_run_leakcheck, QtCore.Qt.LeftButton)
    qtbot.wait_until(window.self_test._btn_continue.isEnabled, timeout = 10000)

    # Press the continue button and start the Flow check
    qtbot.mouseClick(window.self_test._btn_continue, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.self_test.btn_run_spiro_dir, QtCore.Qt.LeftButton)
    qtbot.wait_until(window.self_test._btn_continue.isEnabled, timeout=10000)

    # Press the continue button and start the Change battery check
    qtbot.mouseClick(window.self_test._btn_continue, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.self_test.btn_run_backup_battery, QtCore.Qt.LeftButton)
    qtbot.wait_until(window.self_test._btn_continue.isEnabled, timeout=10000)

    # Press the continue button and go to the Alarm-System check
    qtbot.mouseClick(window.self_test._btn_continue, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.self_test.btn_run_alarmsystem_1, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.messagebar.button_confirm, QtCore.Qt.LeftButton)
    assert "Failure" in window.self_test.endstatus_label_asc_1.text() or "Success" in window.self_test.endstatus_label_asc_1.text()

    qtbot.mouseClick(window.self_test.btn_run_alarmsystem_2, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.messagebar.button_confirm, QtCore.Qt.LeftButton)
    assert "Failure" in window.self_test.endstatus_label_asc_2.text() or "Success" in window.self_test.endstatus_label_asc_2.text()

    qtbot.mouseClick(window.self_test.btn_run_alarmsystem_3, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.messagebar.button_confirm, QtCore.Qt.LeftButton)
    assert "Failure" in window.self_test.endstatus_label_asc_3.text() or "Success" in window.self_test.endstatus_label_asc_3.text()

    # Come back to the previous panel
    previousPageNumber = window.self_test._current_page
    qtbot.mouseClick(window.self_test._btn_back, QtCore.Qt.LeftButton)
    assert window.self_test._current_page == previousPageNumber-1

    # Return to the menu window
    qtbot.mouseClick(window.messagebar.button_cancel, QtCore.Qt.LeftButton)


"""
TS56
"""
def test_selftTest_2(qtbot):
    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)

    # Open the Self Test section
    qtbot.mouseClick(window.button_spiro_calib, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.spiro_calib

    # Start the calibration
    qtbot.mouseClick(window.spiro_calib.start_calibration, QtCore.Qt.LeftButton)
    qtbot.wait_until(lambda: window.spiro_calib.endstatus_label.text() == "Success", timeout=20000)

    # Return to the menu window
    qtbot.mouseClick(window.messagebar.button_cancel, QtCore.Qt.LeftButton)

"""
TS62
"""
def test_selftTest_3(qtbot):

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_new_patient, QtCore.Qt.LeftButton)

    # Open the Self Test section
    qtbot.mouseClick(window.button_start_test, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.self_test

    # Press the Leak check button
    qtbot.mouseClick(window.self_test.btn_run_leakcheck, QtCore.Qt.LeftButton)
    qtbot.wait_until(window.self_test._btn_continue.isEnabled, timeout = 10000)

    # Press the continue button and start the Flow check
    qtbot.mouseClick(window.self_test._btn_continue, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.self_test.btn_run_spiro_dir, QtCore.Qt.LeftButton)
    qtbot.wait_until(window.self_test._btn_continue.isEnabled, timeout=10000)

    # Press the continue button and start the Change battery check
    qtbot.mouseClick(window.self_test._btn_continue, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.self_test.btn_run_backup_battery, QtCore.Qt.LeftButton)
    qtbot.wait_until(window.self_test._btn_continue.isEnabled, timeout=10000)

    # Press the continue button and go to the Alarm-System check, which fails
    qtbot.mouseClick(window.self_test._btn_continue, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.self_test.btn_run_alarmsystem_1, QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.messagebar.button_cancel, QtCore.Qt.LeftButton)
    assert "Failure" in window.self_test.endstatus_label_asc_1.text()

    # Return to the menu window and check that the proceed button is disabled
    qtbot.mouseClick(window.messagebar.button_cancel, QtCore.Qt.LeftButton)
    assert window.button_start_vent.isEnabled() == False
