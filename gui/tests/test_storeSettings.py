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
TS27
"""
def test_storeSettings(qtbot):

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

    # Change the location of the settings file
    config["settings_file_path"] = "./settings.txt"
    window.config = config
    window.settings.send_values_to_hardware()

    assert os.path.exists(config["settings_file_path"])


"""
TS28
"""
def test_loadSettings(qtbot):
    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    assert config is not None
    # Change the location of the settings file
    config["settings_file_path"] = "./settings.txt"

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    window.show()
    qtbot.mouseClick(window.button_resume_patient, QtCore.Qt.LeftButton)
    assert window.toppane.currentWidget() == window.startup

    # Remove the temporary configuration file
    os.remove(config["settings_file_path"])


