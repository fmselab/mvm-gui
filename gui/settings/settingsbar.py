#!/usr/bin/env python3
"""
Settings bar helper
"""

import os
from PyQt5 import QtWidgets, uic


class SettingsBar(QtWidgets.QWidget):
    """
    Settings bar class
    """

    def __init__(self, *args):
        """
        Initialize the SettingsBar container widget.

        Provides a passthrough to underlying widgets.
        """
        super(SettingsBar, self).__init__(*args)
        uifile = os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            "settingsbar.ui")

        uic.loadUi(uifile, self)
