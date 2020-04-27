#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from .mvm_basics import *
from mainwindow import MainWindow
from frozenplots.frozenplots import *
from PyQt5.QtCore import QCoreApplication


"""
TH09
"""
def test_cursorShow(qtbot):
    '''
    Test the cursors on the plot
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
        
    print(esp32)

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu

    active_plots = []
    for slotname in window.plots:
        active_plots.append(window.plots[slotname])

    cursor = Cursor(active_plots)
    cursor.show_cursors()
    for c in cursor.cursor_x:     assert c.isVisible
    for c in cursor.cursor_y:     assert c.isVisible
    for c in cursor.cursor_label: assert c.isVisible

"""
TH10
"""
def test_cursorDrawLabel(qtbot):
    '''
    Test the labels of the cursors
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    print(esp32)

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu

    active_plots = []
    for slotname in window.plots:
        active_plots.append(window.plots[slotname])

    cursor = Cursor(active_plots)
    for num, plot in enumerate(cursor.plots):
        cursor._y[num] = 10

    cursor.draw_label()

    for num, plot in enumerate(cursor.plots):
        assert str(cursor._y[num]) in cursor.cursor_label[num].textItem.toPlainText()

