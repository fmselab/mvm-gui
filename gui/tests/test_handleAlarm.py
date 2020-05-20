#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
from PyQt5.QtWidgets import *
import pytest
from .mvm_basics import *
import time
from mainwindow import MainWindow
from messagebox import MessageBox
from alarm_handler import AlarmHandler
from alarms.alarmsbar import AlarmsBar
from PyQt5.QtCore import QCoreApplication


"""
TH08
"""
def test_objectCreation(qtbot):
    '''
    Test the creation of the AlarmHandler instance
    '''

    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    bar = AlarmsBar()
    handler = AlarmHandler(config, esp32, window.alarmbar, None)

    assert handler is not None

