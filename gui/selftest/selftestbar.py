#!/usr/bin/env python3
"""
Self test bar helper.
"""

import os
from PyQt5 import QtWidgets, uic


class SelfTestBar(QtWidgets.QWidget):
    """
    SelfTestBar bar class
    """

    def __init__(self, *args):
        """
        Initialize the SelfTestBar widget.

        Grabs child widgets.
        """
        super(SelfTestBar, self).__init__(*args)
        uifile = os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
                              "selftestbar.ui")

        uic.loadUi(uifile, self)
