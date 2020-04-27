#!/usr/bin/env python3
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore
import os

from menu.menu import Menu

class Toolbar(QtWidgets.QWidget):
    def __init__(self, *args):
        """
        Initialize the Toolbar container widget.

        Provides a passthrough to underlying widgets.
        """
        super(Toolbar, self).__init__(*args)
        uic.loadUi(os.environ['MVMGUI'] + "toolbar/toolbar.ui", self)

        self.label_status = self.findChild(QtWidgets.QLabel, "label_status")
        self.button_unlockscreen = self.findChild(QtWidgets.QPushButton, "button_unlockscreen")

        self.button_unlockscreen.blinkstate = True

        self.blinktimer = QtCore.QTimer(self)
        self.blinktimer.setInterval(500) #.5 seconds
        self.blinktimer.timeout.connect(self.blink_unlock)
        self.blinktimer.start()
        self.set_stopped("PCV")

    def set_stopped(self, mode_text=""):
        self.label_status.setText("Status: Stopped\n" + mode_text)
        self.label_status.setStyleSheet(
                "QLabel { background-color : red; color: yellow;}");

    def set_running(self, mode_text=""):
        self.label_status.setText("Status: Running\n" + mode_text)
        self.label_status.setStyleSheet(
                "QLabel { background-color : green;  color: yellow;}");

    def blink_unlock(self):
        button = self.button_unlockscreen
        if button.blinkstate:
            color = "#aaaaaa"
            button.blinkstate = False
        else:
            color = "#ffffff"
            button.blinkstate = True

        palette = button.palette()
        role = button.backgroundRole()
        palette.setColor(role, QtGui.QColor(color))
        button.setPalette(palette)

