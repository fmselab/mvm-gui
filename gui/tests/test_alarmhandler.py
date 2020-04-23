#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
from PyQt5.QtWidgets import *
import pytest
from .mvm_basics import *
from mainwindow import MainWindow
from gui.messagebox import MessageBox
from gui.alarm_handler import AlarmHandler
from PyQt5.QtCore import QCoreApplication

def test_objectCreation(qtbot):
    '''
    Test the creation of the AlarmHandler instance
    '''

    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    handler = AlarmHandler(config, esp32)

    assert handler is not None

