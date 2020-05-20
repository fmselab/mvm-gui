#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from .mvm_basics import *
from mainwindow import MainWindow
from frozenplots.frozenplots import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication
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


"""
TS29
"""
def test_frozenPlotY(qtbot):
    '''
    Test the alteration of the frozen plot on the Y axis
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu

    # Special Operations
    qtbot.mouseClick(window.button_specialops, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.specialbar

    assert window.esp32.get_all() != ""

    # Freeze plots
    qtbot.mouseClick(window.specialbar.button_freeze, QtCore.Qt.LeftButton)
    assert window.data_filler._frozen == True
    assert window.rightbar.currentWidget() == window.frozen_right
    assert window.bottombar.currentWidget() == window.frozen_bot

    # Try to zoom the plot on the y axis
    range = window.plots['plot_top'].getViewBox().viewRange()
    qtbot.mouseClick(window.frozen_right.yzoom_top.button_plus, QtCore.Qt.LeftButton)
    assert range < window.plots['plot_top'].getViewBox().viewRange()

    # Try to unzoom the plot on the y axis
    range = window.plots['plot_top'].getViewBox().viewRange()
    qtbot.mouseClick(window.frozen_right.yzoom_top.button_minus, QtCore.Qt.LeftButton)
    assert range > window.plots['plot_top'].getViewBox().viewRange()

    # Move the plot in the UP direction
    range = window.plots['plot_top'].getViewBox().viewRange()
    qtbot.mouseClick(window.frozen_right.yzoom_top.button_up, QtCore.Qt.LeftButton)
    assert range < window.plots['plot_top'].getViewBox().viewRange()

    # Move the plot in the DOWN direction
    range = window.plots['plot_top'].getViewBox().viewRange()
    qtbot.mouseClick(window.frozen_right.yzoom_top.button_down, QtCore.Qt.LeftButton)
    assert range > window.plots['plot_top'].getViewBox().viewRange()


"""
TS30
"""
def test_frozenPlotX(qtbot):
    '''
    Test the alteration of the frozen plot on the X axis
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu

    # Special Operations
    qtbot.mouseClick(window.button_specialops, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.specialbar

    # Freeze plots
    qtbot.mouseClick(window.specialbar.button_freeze, QtCore.Qt.LeftButton)
    assert window.data_filler._frozen == True
    assert window.rightbar.currentWidget() == window.frozen_right
    assert window.bottombar.currentWidget() == window.frozen_bot

    # Try to zoom the plot on the x axis
    range = window.plots['plot_top'].getViewBox().viewRange()
    qtbot.mouseClick(window.frozen_bot.xzoom.button_plus, QtCore.Qt.LeftButton)
    assert range < window.plots['plot_top'].getViewBox().viewRange()

    # Try to unzoom the plot on the y axis
    range = window.plots['plot_top'].getViewBox().viewRange()
    qtbot.mouseClick(window.frozen_bot.xzoom.button_minus, QtCore.Qt.LeftButton)
    assert range > window.plots['plot_top'].getViewBox().viewRange()

    # Move the plot in the RIGHT direction
    range = window.plots['plot_top'].getViewBox().viewRange()
    qtbot.mouseClick(window.frozen_bot.xzoom.button_right, QtCore.Qt.LeftButton)
    assert range < window.plots['plot_top'].getViewBox().viewRange()

    # Move the plot in the LEFT direction
    range = window.plots['plot_top'].getViewBox().viewRange()
    qtbot.mouseClick(window.frozen_bot.xzoom.button_left, QtCore.Qt.LeftButton)
    assert range > window.plots['plot_top'].getViewBox().viewRange()
