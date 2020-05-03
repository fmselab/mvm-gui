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
        self._esp32 = None
        self._mainwindow = None
        self._selftestbar = None
        self._btn_continue = None
        self._btn_back = None
        self._btn_abort = None

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
        self.btn_run_alarmsystem_1.clicked.connect(self.run_alarmsystem_1)
        self.btn_run_alarmsystem_2.clicked.connect(self.run_alarmsystem_2)
        self.btn_run_alarmsystem_3.clicked.connect(self.run_alarmsystem_3)

    def _enable_bar_buttons(self, enabled=True):
        self._btn_back.setEnabled(enabled)
        self._btn_continue.setEnabled(enabled)
        self._btn_abort.setEnabled(enabled)

    def run_leak_check(self):
        '''
        Runs the leak check test
        '''

        self._enable_bar_buttons(False)
        self.btn_run_leakcheck.setEnabled(False)
        self.endstatus_label.setText("")
        self.completion_bar.setValue(0)

        try:
            retriever = self._esp32.leakage_test()

            patient_ps = []
            internal_ps = []

            for competion, internal_p, patient_p in retriever.data():
                self.completion_bar.setValue(completion)
                patient_ps.append(patient_p)
                internal_ps.append(internal_p)

            if abs(patient_ps[0] - patient_ps[-1]) < 10:
                raise Exception("Check failed")

            self.endstatus_label.setText("Succeeded")
        except:
            self.endstatus_label.setText("Failed")
        finally:
            self._enable_bar_buttons()
            self.btn_run_leakcheck.setEnabled(True)
            del retriever

    def run_spiro_dir(self):
        '''
        Runs the spirometer direction test
        '''
        # TODO: to be implemented
        print('Running run_spiro_dir')
        return

    def run_backup_battery(self):
        '''
        Runs the backup battery test
        '''
        # TODO: to be implemented
        print('Running run_backup_battery')
        return

    def run_alarmsystem_1(self):
        '''
        Runs the alarm system test
        '''
        # TODO: to be implemented
        print('Running run_alarmsystem')
        return

    def run_alarmsystem_2(self):
        '''
        Runs the alarm system test
        '''
        # TODO: to be implemented
        print('Running run_alarmsystem')
        return

    def run_alarmsystem_3(self):
        '''
        Runs the alarm system test
        '''
        # TODO: to be implemented
        print('Running run_alarmsystem')
        return
