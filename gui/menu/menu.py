#!/usr/bin/env python3
"""
Menu bar helper.
"""

import os
from PyQt5 import QtWidgets, uic


class Menu(QtWidgets.QWidget):
    """
    Menu bar class
    """

    def __init__(self, *args):
        """
        Initialize the Menu widget.

        Grabs child widgets.
        """
        super(Menu, self).__init__(*args)
        uifile = os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            "menu.ui")

        uic.loadUi(uifile, self)
