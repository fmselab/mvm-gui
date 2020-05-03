#!/usr/bin/env python3
'''
This module implements the self-test procedure and its user wizard.
'''

import os
from PyQt5 import QtWidgets, uic


class SelfTest(QtWidgets.QWidget):
    '''
    SelfTest widget. User guidance through the procedure.
    '''
    def __init__(self, *args):
        """
        Constructor. Initializes the SelfTest widget.
        """

        super(SelfTest, self).__init__(*args)
        uifile = os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            "selftest.ui")

        uic.loadUi(uifile, self)

        self._all_pages = [
            self.page_leakcheck,
            self.page_spiro_dir,
            self.page_backupbattery,
            self.page_alarmsystem
        ]

        self._current_page = None

    def go_to_next_page(self):
        '''
        Goes to the next page
        '''

        self._current_page += 1
        
        if self._current_page >= len(self._all_pages):
            raise Exception('Can\t go to next page.')
        
        self.stack.setCurrentWidget(self._all_pages[self._current_page])

        self.update_enabled_buttons()

    def go_to_previous_page(self):
        '''
        Goes to the previous page
        '''

        self._current_page -= 1
        
        if self._current_page < 0:
            raise Exception('Can\t go to previous page.')
        
        self.stack.setCurrentWidget(self._all_pages[self._current_page])

        self.update_enabled_buttons()

    def update_enabled_buttons(self):
        '''
        Check if we can go next of back,
        and if we cannot it disable either 
        the continue of the back buttons
        '''

        if self._current_page == 0:
            self._btn_back.setEnabled(False)
        else:
            self._btn_back.setEnabled(True)

        if self._current_page == len(self._all_pages)-1:
            self._btn_continue.setEnabled(False)
        else:
            self._btn_continue.setEnabled(True)

        self._btn_continue.repaint()
        self._btn_back.repaint()

    def connect_mainwindow_esp32_selftestbar(self, mainwindow, esp32, selftestbar):
        """
        Connect the ESP32Serial istance.
        """

        self._esp32 = esp32
        self._mainwindow = mainwindow
        self._selftestbar = selftestbar

        self._btn_continue = self._selftestbar.button_continue
        self._btn_back = self._selftestbar.button_back
        self._btn_abort = self._selftestbar.button_abort

        self._btn_continue.clicked.connect(self.go_to_next_page)
        self._btn_back.clicked.connect(self.go_to_previous_page)

        self._current_page = -1
        self.go_to_next_page()

        self.btn_run_leakcheck.clicked.connect(self.run_leak_check)
        self.btn_run_spiro_dir.clicked.connect(self.run_spiro_dir)
        self.btn_run_backup_battery.clicked.connect(self.run_backup_battery)
        self.btn_run_alarmsystem.clicked.connect(self.run_alarmsystem)

    def run_leak_check(self):
        '''
        Runs the leak check test
        '''
        print('Running run_leak_check')
        return

    def run_spiro_dir(self):
        '''
        Runs the spirometer direction test
        '''
        print('Running run_spiro_dir')
        return

    def run_backup_battery(self):
        '''
        Runs the backup battery test
        '''
        print('Running run_backup_battery')
        return

    def run_alarmsystem(self):
        '''
        Runs the alarm system test
        '''
        print('Running run_alarmsystem')
        return

