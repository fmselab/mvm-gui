#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from .mvm_basics import *
from communication.esp32serial import *
import serial  # pySerial
from PyQt5.QtCore import QCoreApplication

"""
TH24
"""
def test_newException(qtbot):
    exception = ESP32Exception("Get", "1", "Prova")
    assert exception.line == "1"

    try:
        raise exception
    except ESP32Exception:
        pass

"""
TH25
"""
def test_newSerial(qtbot):
    try:
        seriale = ESP32Serial(config)
        assert seriale.get_all_fields == config["get_all_fields"]
    except serial.SerialException:
        pass
    except ESP32Exception:
        pass

