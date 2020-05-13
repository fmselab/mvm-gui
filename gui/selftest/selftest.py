#!/usr/bin/env python3
'''
This module implements the self-test procedure and its user wizard.
'''

import os
import time
from communication.rpi import start_alarm_system, stop_alarm_system
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
        self._btn_cancel = None

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
        self._btn_cancel = self._selftestbar.button_cancel

        self._btn_continue.clicked.connect(self.go_to_next_page)
        self._btn_back.clicked.connect(self.go_to_previous_page)
        self._btn_cancel.clicked.connect(self._mainwindow.goto_new_patient)

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
        self._btn_cancel.setEnabled(enabled)
        if enabled:
            self.update_enabled_buttons()

    def run_leak_check(self):
        '''
        Runs the leak check test
        '''

        self._enable_bar_buttons(False)
        self.btn_run_leakcheck.setEnabled(False)
        self.endstatus_label_lc.setText("")
        self.completion_bar_lc.setValue(0)

        retriever = None
        try:
            retriever = self._esp32.leakage_test()

            patient_ps = []
            internal_ps = []

            for completion, internal_p, patient_p in retriever.data():
                self.completion_bar_lc.setValue(completion)
                patient_ps.append(patient_p)
                internal_ps.append(internal_p)

            if abs(patient_ps[0] - patient_ps[-1]) < 10:
                raise Exception("Check failed")

            self.endstatus_label_lc.setText("Success")
        except:
            self.endstatus_label_lc.setText("Failure")
        finally:
            self._enable_bar_buttons()
            self.btn_run_leakcheck.setEnabled(True)
            if retriever:
                del retriever

    def run_spiro_dir(self):
        '''
        Runs the spirometer direction test
        '''
        self.btn_run_spiro_dir.setEnabled(False)
        self._enable_bar_buttons(False)
        self.endstatus_label_fdc.setText("")

        try:
            # get the current mode and respiratory rate
            mode = self._esp32.get("mode")
            rate = self._esp32.get("rate")

            # set test rate, mode and run
            self._esp32.set("rate", 20)
            self._esp32.set("mode", 0)
            self._esp32.set("run", 1)

            now = time.time()
            test_start = now
            test_stop = now + 20

            while now < test_stop:
                completion = 100. * (now - test_start) / 20
                self.completion_bar_fdc.setValue(completion)
                time.sleep(1)
                now = time.time()

            self._esp32.set("run", 0)
            self._esp32.set("mode", mode)
            self._esp32.set("rate", rate)

            if (1 << 23) in self._esp32.get_alarms().get_alarm_codes():
                self.endstatus_label_fdc.setText("Failure")
            else:
                self.endstatus_label_fdc.setText("Success")
        except:
            self.endstatus_label_fdc.setText("Failure")

        self._enable_bar_buttons()
        self.btn_run_spiro_dir.setEnabled(True)

    def _confirm_battery_warning(self, success):
        self._enable_bar_buttons()
        self.btn_run_backup_battery.setEnabled(True)
        if success:
            self.endstatus_label_bc.setText("Success")
        else:
            self.endstatus_label_bc.setText("Failure")

    def run_backup_battery(self):
        '''
        Runs the backup battery test
        '''
        self.btn_run_backup_battery.setEnabled(False)
        self._enable_bar_buttons(False)
        self.endstatus_label_bc.setText("")

        counter = 0
        while counter != 10*20:
            counter += 1
            warnings = self._esp32.get_warnings().get_alarm_codes()
            if (1 << 1) in warnings:
                break
            self.repaint()
            time.sleep(0.05)

        if counter == 200:
            self._confirm_battery_warning(False)
            return

        self._mainwindow.messagebar.get_confirmation(
                "Confirm the warning worked or not",
                "Is the buzzer sounding and the LED flashing?",
                color="white",
                func_confirm=lambda: self._confirm_battery_warning(True),
                func_cancel=lambda: self._confirm_battery_warning(False))


    def _enable_alarm_test_buttons(self, enabled=True):
        """
        Allows to enable or disable alarm system buttons at once
        """

        self.btn_run_alarmsystem_1.setEnabled(enabled)
        self.btn_run_alarmsystem_2.setEnabled(enabled)
        self.btn_run_alarmsystem_3.setEnabled(enabled)

    def _confirm_alarm_test_1(self, success):
        self._esp32.set("alarm_test", 0)
        self._enable_bar_buttons()
        self._enable_alarm_test_buttons()
        if success:
            self.endstatus_label_asc_1.setText("Success")
        else:
            self.endstatus_label_asc_1.setText("Failure")

    def _confirm_alarm_test_2(self, success):
        self._esp32.set("alarm_test", 0)
        self._enable_bar_buttons()
        self._enable_alarm_test_buttons()
        if success:
            self.endstatus_label_asc_2.setText("Success")
        else:
            self.endstatus_label_asc_2.setText("Failure")

    def _confirm_alarm_test_3(self, success):
        stop_alarm_system()
        self._enable_bar_buttons()
        self._enable_alarm_test_buttons()
        if success:
            self.endstatus_label_asc_3.setText("Success")
        else:
            self.endstatus_label_asc_3.setText("Failure")

    def run_alarmsystem_1(self):
        '''
        Runs the alarm system test number 1
        '''
        self._enable_alarm_test_buttons(False)
        self._enable_bar_buttons(False)
        self.endstatus_label_asc_1.setText("")

        self._esp32.set("alarm_test", 1)
        counter = 0
        while counter != 2*20:
            counter += 1
            alarms = self._esp32.get_alarms().get_alarm_codes()
            if (1 << 28) in alarms:
                break
            self.repaint()
            time.sleep(0.05)

        if counter == 40:
            self._confirm_alarm_test_1(False)
            return

        self._mainwindow.messagebar.get_confirmation(
                "Confirm the warning worked or not",
                "Is the buzzer sounding and the LED flashing?",
                color="white",
                func_confirm=lambda: self._confirm_alarm_test_1(True),
                func_cancel=lambda: self._confirm_alarm_test_1(False))

    def run_alarmsystem_2(self):
        '''
        Runs the alarm system test number 2
        '''
        self._enable_alarm_test_buttons(False)
        self._enable_bar_buttons(False)
        self.endstatus_label_asc_2.setText("")

        self._esp32.set("alarm_test", 2)

        self._mainwindow.messagebar.get_confirmation(
                "Confirm the warning worked or not",
                "Is the buzzer sounding and the LED flashing?",
                color="white",
                func_confirm=lambda: self._confirm_alarm_test_2(True),
                func_cancel=lambda: self._confirm_alarm_test_2(False))

    def run_alarmsystem_3(self):
        '''
        Runs the alarm system test number 3
        '''
        self._enable_alarm_test_buttons(False)
        self._enable_bar_buttons(False)
        self.endstatus_label_asc_3.setText("")

        start_alarm_system()

        self._mainwindow.messagebar.get_confirmation(
                "Confirm the warning worked or not",
                "Is the buzzer sounding and the LED flashing?",
                color="white",
                func_confirm=lambda: self._confirm_alarm_test_3(True),
                func_cancel=lambda: self._confirm_alarm_test_3(False))
