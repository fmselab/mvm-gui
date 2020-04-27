#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from .mvm_basics import *
from mainwindow import MainWindow
from gui.controller_status import ControllerStatus
from start_stop_worker import StartStopWorker
from PyQt5.QtCore import QCoreApplication

def test_basics(qtbot):
    '''
    Basic test that works more like a sanity check 
    to ensure we are setting up a QApplication properly
    '''
    assert qt_api.QApplication.instance() is not None

    widget = qt_api.QWidget()
    qtbot.addWidget(widget)
    widget.setWindowTitle("W1")
    widget.show()

    assert widget.isVisible()
    assert widget.windowTitle() == "W1"

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
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu

    work = StartStopWorker(window, config, esp32, window.button_startstop,
            window.button_autoassist, window.toolbar, window.settings)

    assert "Stopped" in work.toolbar.label_status.text() and "PCV" in work.toolbar.label_status.text()

    work.start_button_pressed()

    qtbot.waitUntil(lambda: "Running" in work.toolbar.label_status.text() and "PCV" in work.toolbar.label_status.text(), timeout=5000)
    assert True

    assert window.button_autoassist.isEnabled() == False

    # Change the modality
    work.toggle_mode()

    assert "Stopped" in work.toolbar.label_status.text() and "PSV" in work.toolbar.label_status.text()
    work.toggle_start_stop()
    work.start_button_pressed()

    qtbot.waitUntil(lambda: "Running" in work.toolbar.label_status.text() and "PSV" in work.toolbar.label_status.text(), timeout=5000)
    assert True

    assert work.is_running()

