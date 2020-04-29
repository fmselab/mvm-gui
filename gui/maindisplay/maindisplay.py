#!/usr/bin/env python3
"""
Main window helper
"""

import os
from PyQt5 import QtWidgets, uic


class MainDisplay(QtWidgets.QWidget):
    """
    Main window class
    """

    def __init__(self, *args):
        """
        Initialize the MainDisplay container widget.

        Provides a passthrough to underlying widgets.
        """
        super(MainDisplay, self).__init__(*args)
        uic.loadUi(os.environ['MVMGUI'] + "maindisplay/maindisplay.ui", self)
