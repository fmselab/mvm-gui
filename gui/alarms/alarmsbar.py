#!/usr/bin/env python3
"""
Alarm bar helper
"""

import os
from PyQt5 import QtWidgets, uic


class AlarmsBar(QtWidgets.QWidget):
    """
    Alarm bar class
    """

    def __init__(self, *args):
        """
        Initialize the AlarmsBar widget.

        Grabs child widgets.
        """
        super(AlarmsBar, self).__init__(*args)
        uic.loadUi(os.environ['MVMGUI'] + "alarms/alarmsbar.ui", self)

