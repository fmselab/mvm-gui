#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from .mvm_basics import *
from mainwindow import MainWindow
from toolsettings.toolsettings import ToolSettings
from PyQt5.QtCore import QCoreApplication


"""
TH04
"""
def test_setupWithUnits(qtbot):
    '''
    Test the creation of the ToolSettings instance with name and units
    '''

    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    settings = ToolSettings()

    settings.setup("Prova", units="a")

    assert settings.label_name.text() == "Prova"
    assert settings.label_units.text() == "a"

"""
TH05
"""
def test_setupWithoutUnits(qtbot):
    '''
    Test the creation of the ToolSettings instance with name but without units
    '''

    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    settings = ToolSettings()

    settings.setup("Prova")

    assert settings.label_name.text() == "Prova"
    assert settings.label_units.text() == ""


"""
TS31
"""
def test_checkToolSettings(qtbot):
    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    # Check the toolSettings on the mainn window
    assert window.toolsettings["toolsettings_1"].labels["name"].text() == "Resp. Rate"
    assert window.toolsettings["toolsettings_2"].labels["name"].text() == "Insp./Expir."