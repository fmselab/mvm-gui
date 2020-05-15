#!/usr/bin/env python3
"""
Settings ui helper
"""

import os
import sys
import copy
from PyQt5 import QtWidgets, uic
from presets.presets import Presets
from .settingsfile import SettingsFile


class Settings(QtWidgets.QMainWindow):
    #pylint: disable=too-many-instance-attributes
    """
    GUI tool for letting the user see and enter the operational parameter
    of the ventilator.
    """

    def __init__(self, mainparent, *args):
        """
        Initialized the Settings overlay widget.
        """
        super(Settings, self).__init__(*args)
        uifile = os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            "settings.ui")

        uic.loadUi(uifile, self)

        self._debug = True
        self.mainparent = mainparent

        # Get access to parent widgets and data
        self._config = self.mainparent.config
        self._data_h = self.mainparent._data_h
        self._toolsettings = self.mainparent.toolsettings
        self._messagebar = self.mainparent.messagebar
        # self._start_stop_worker = self.mainparent._start_stop_worker

        # This contains all the default params
        self._current_values = {}
        self._current_values_temp = {}

        self._all_spinboxes = {
            # General
            'leak_compensation': self.spinBox_leak_compensation,
            # Auto
            'respiratory_rate': self.spinBox_rr,
            'insp_expir_ratio': self.spinBox_insp_expir_ratio,
            'insp_pressure': self.spinBox_insp_pressure,
            'pcv_trigger_enable': self.toggle_pcv_trigger_enable,
            'pcv_trigger_pressure': self.spinBox_trigger_sensitivity,
            # Assist
            'pressure_trigger': self.spinBox_pressure_trigger,
            'flow_trigger': self.spinBox_flow_trigger,
            'support_pressure': self.spinBox_support_pressure,
            'max_apnea_time': self.spinBox_max_apnea_time,
            'enable_backup': self.toggle_enable_backup,
            'apnea_rr': self.spinBox_apnea_rr,
            'apnea_insp_press': self.spinBox_apnea_insp_press,
            # Lung recruit
            'lung_recruit_pres': self.spinBox_lr_p,
            'lung_recruit_time': self.spinBox_lr_t,
        }

        self._all_fakebtn = {
            # General
            'leak_compensation': self.fake_btn_leak_compensation,
            # Auto
            'respiratory_rate': self.fake_btn_rr,
            'insp_expir_ratio': self.fake_btn_ie,
            'insp_pressure': self.fake_btn_insp_pressure,
            'pcv_trigger_pressure': self.fake_btn_trigger_sensitivity,
            # Assist
            'pressure_trigger': self.fake_btn_pr_trigger,
            'flow_trigger': self.fake_btn_flow_trig,
            'support_pressure': self.fake_btn_support_pressure,
            'max_apnea_time': self.fake_btn_max_apnea_time,
            'apnea_rr': self.fake_btn_apnea_rr,
            'apnea_insp_press': self.fake_btn_apnea_insp_press,
            # Lung recruit
            'lung_recruit_pres': self.fake_btn_lr_p,
            'lung_recruit_time': self.fake_btn_lr_t
        }

        self._all_spinboxes['respiratory_rate'].valueChanged.connect(
            self._recalculate_inspiratory_time)
        self._all_spinboxes['insp_expir_ratio'].valueChanged.connect(
            self._recalculate_inspiratory_time)

        self.toolsettings_lookup = {}

        # Connect all widgets
        self.connect_workers()

        # Init presets
        self._current_preset = None
        self._current_preset_name = None

        # Default to PCV setup; will be updated by start_stop_worker.
        self.set_pcv()
        self.load_presets()

    def _recalculate_inspiratory_time(self):
        rrate = self._all_spinboxes['respiratory_rate'].value()
        expr_denon = self._all_spinboxes['insp_expir_ratio'].value()
        self.inspiratory_time_label.setText(
            "%.2f" % (60.0 / (rrate * (1 + expr_denon))))

    def spawn_presets_window(self, name):
        """
        Opens the preset overlay for the given parameter name.

        arguments:
        - name: the parameter name.
        """
        presets = self._config[name]['presets']

        self._current_preset_name = name

        if self._current_preset is not None:
            self._current_preset.close()

        self._current_preset = Presets(presets, self)
        self._current_preset.show()
        self._current_preset.button_cancel.pressed.connect(
            self.hide_preset_worker)
        for btn in self._current_preset.button_preset:
            btn.pressed.connect(self.preset_worker)

        self.inactivate_settings_buttons()

        # Always set the focus to the tab
        self.tabs.setFocus()

    def hide_preset_worker(self):
        '''
        Callback to close the preset overlay.
        '''
        self._current_preset.hide()
        self.activate_settings_buttons()

        # Reset the Settings window
        self.repaint()

        # Always set the focus to the tab
        self.tabs.setFocus()

    def preset_worker(self):
        """
        Callback to accept a value from the preset overlay.
        """

        value = self.sender().text()
        value = value.split(' ')[0]
        value = float(value)

        self._all_spinboxes[self._current_preset_name].setValue(value)
        self._current_values_temp[self._current_preset_name] = value

        self.hide_preset_worker()

    def inactivate_settings_buttons(self):
        '''
        Inactivates all in the settings window
        '''
        self.tabs.setDisabled(True)

    def activate_settings_buttons(self):
        '''
        Activates all in the settings window
        '''
        self.tabs.setEnabled(True)

    def connect_workers(self):
        '''
        Connects all the buttons, inputs, etc
        to the the appropriate working functions
        '''
        # Shared apply, close, preset buttons
        self._button_apply = self.mainparent.settingsbar.findChild(
            QtWidgets.QPushButton, "button_apply")
        self._button_close = self.mainparent.settingsbar.findChild(
            QtWidgets.QPushButton, "button_close")
        self._button_loadpreset = self.mainparent.settingsbar.findChild(
            QtWidgets.QPushButton, "button_loadpreset")

        self._button_apply.clicked.connect(self.apply_worker)
        self._button_loadpreset.clicked.connect(self.load_presets)
        self._button_close.clicked.connect(self.close_settings_worker)

        # General
        self._all_fakebtn['leak_compensation'].clicked.connect(
            lambda: self.spawn_presets_window('leak_compensation'))

        # Auto
        self._all_fakebtn['respiratory_rate'].clicked.connect(
            lambda: self.spawn_presets_window('respiratory_rate'))
        self._all_fakebtn['insp_expir_ratio'].clicked.connect(
            lambda: self.spawn_presets_window('insp_expir_ratio'))
        self._all_fakebtn['insp_pressure'].clicked.connect(
            lambda: self.spawn_presets_window('insp_pressure'))
        self._all_fakebtn['pcv_trigger_pressure'].clicked.connect(
            lambda: self.spawn_presets_window('pcv_trigger_pressure'))

        # Assist
        self._all_fakebtn['pressure_trigger'].clicked.connect(
            lambda: self.spawn_presets_window('pressure_trigger'))
        self._all_fakebtn['flow_trigger'].clicked.connect(
            lambda: self.spawn_presets_window('flow_trigger'))
        self._all_fakebtn['support_pressure'].clicked.connect(
            lambda: self.spawn_presets_window('support_pressure'))
        self._all_fakebtn['max_apnea_time'].clicked.connect(
            lambda: self.spawn_presets_window('max_apnea_time'))
        self._all_fakebtn['apnea_rr'].clicked.connect(
            lambda: self.spawn_presets_window('apnea_rr'))
        self._all_fakebtn['apnea_insp_press'].clicked.connect(
            lambda: self.spawn_presets_window('apnea_insp_press'))

        # Lung recruitment
        self._all_fakebtn['lung_recruit_pres'].clicked.connect(
            lambda: self.spawn_presets_window('lung_recruit_pres'))
        self._all_fakebtn['lung_recruit_time'].clicked.connect(
            lambda: self.spawn_presets_window('lung_recruit_time'))

        for param, btn in self._all_spinboxes.items():
            if param in ['enable_backup', 'pcv_trigger_enable']:
                btn.clicked.connect(self.worker)
            else:
                btn.valueChanged.connect(self.worker)

        # Special operations
        self.label_warning.setVisible(False)
        self.btn_sw_update.clicked.connect(lambda: self._messagebar.get_confirmation(
            "Confirm SOFTWARE UPDATE AND CLOSE",
            "Are you sure you want to request and execute a SOFTWARE UPDATE and CLOSE?",
            func_confirm=self.upgrade_and_exit,
            color="red"))

    def upgrade_and_exit(self):
        cmd = self._config['upgrade_script']

        print("Running \"%s\"..." % cmd)
        os.system(cmd)
        print("Complete. Closing GUI.")
        sys.exit(0)

    def load_presets(self):
        '''
        Loads the presets from the config file
        '''

        for param, btn in self._all_spinboxes.items():
            value_config = self._config[param]

            if param not in ['enable_backup', 'pcv_trigger_enable']:
                btn.setMinimum(value_config['min'])
                btn.setMaximum(value_config['max'])
                btn.setSingleStep(value_config.get('step', 0.1))

            btn.setValue(value_config['default'])
            self._current_values[param] = value_config['default']


        self._current_values_temp = copy.copy(self._current_values)

        self.repaint()

    def set_pcv(self):
        """
        Inform that the current ventilation mode is PCV
        """

        self._set_mode("pcv")

    def set_psv(self):
        """
        Inform that the current ventilation mode is PSV
        """

        self._set_mode("psv")

    def _set_mode(self, mode):
        """
        Set the mode to PSV or PCV depending on the parameter and sets the
        toolsetting shown in the bottom bar.

        Arguments:
        - mode (string): 'psv' or 'pcv'
        """

        tool_list = self._config["displayed_toolsettings"][mode]

        self.toolsettings_lookup = {}

        # At most 3 tools can be shown
        len_tool_list = len(tool_list)
        for idx in range(3):
            widget = self._toolsettings["toolsettings_%d" % (idx + 1)]

            if len_tool_list > idx:
                # Show the widget and assign an easy lookup
                widget.load_presets(tool_list[idx])
                self.toolsettings_lookup[tool_list[idx]] = widget
            else:
                # Hide the widget
                widget.load_presets(None)

        # When this class is being constructed, we haven't
        # read any values, so will just leave the toolsettings
        # as their default values.
        if self._current_values:
            self.update_toolsettings_values()

    def close_settings_worker(self):
        '''
        Closes the settings window, w/o applying
        any changes to the parameters
        '''
        self._current_values_temp = copy.copy(self._current_values)

        # Restore to previous values
        for param, btn in self._all_spinboxes.items():
            print('Resetting', param, 'to ', self._current_values[param])
            btn.setValue(self._current_values[param])

        self.repaint()
        self.mainparent.exit_settings()

    def update_spinbox_value(self, param, value):
        """
        Set a value to the given spinbox.

        arguments:
        - param: the name of the parameter associated to the spinbox.
        - value: the value to be set.
        """

        if param in self._all_spinboxes:
            self._all_spinboxes[param].setValue(value)
            self._current_values[param] = value
        else:
            raise Exception('Cannot set value to SpinBox with name', param)

    def update_config(self, external_config):
        '''
        Loads the presets from the config file
        '''

        for param, btn in self._all_spinboxes.items():
            if param in external_config:
                value = external_config[param]
            else:
                value = self.config[param]["default"]

            btn.setValue(value)
            self._current_values[param] = value

        self.send_values_to_hardware()

    def apply_worker(self):
        '''
        Applyes the current changes and sends them to the ESP
        '''
        self._current_values = copy.copy(self._current_values_temp)
        self.send_values_to_hardware()
        self.mainparent.exit_settings()

    def send_values_to_hardware(self):
        '''
        Sends the currently set values to the ESP
        '''

        settings_to_file = {}
        for param, btn in self._all_spinboxes.items():
            settings_to_file[param] = self._current_values[param]

            # value is the variable to be sent to the hardware,
            # so possibly converted from the settings
            if param in ['enable_backup', 'pcv_trigger_enable']:
                value = int(self._current_values[param])
            elif param == 'insp_expir_ratio':
                i_over_e = 1. / self._current_values[param]
                value = 1. / (i_over_e + 1)
            else:
                value = self._current_values[param]

            if 'conversion' in self._config[param]:
                value = value * self._config[param]['conversion']
                if self._debug:
                    print('Converting value for', param,
                          'from', value / self._config[param].get('conversion', 1.), 'to', value)

            if self._debug:
                print('Setting value of', param, ':', value)

            # Update the value in the config file
            self._config[param]['current'] = self._current_values[param]

            # Set color to red until we know the value has been set.
            btn.setStyleSheet("color: red")

            esp_param_name = self._config['esp_settable_param'][param]

            # Finally, try to set the value to the ESP
            # Raise an error message if this fails.
            if self._data_h.set_data(esp_param_name, value):
                # Now set the color to green, as we know it has been set
                btn.setStyleSheet("color: green")

        self.update_toolsettings_values()
        settings_file = SettingsFile(self._config["settings_file_path"])
        settings_file.store(settings_to_file)

    def update_toolsettings_values(self):
        '''
        Update the values shown in the bottom toolsettings boxes
        with the current values of the parameters.
        '''
        for param, toolsetting in self.toolsettings_lookup.items():
            toolsetting.update(self._current_values[param])

    def worker(self):
        '''
        This is called when clicking on a SpinBox
        Sets the curently set value in temporary dict
        which will be saved if the user clicks on Apply
        '''
        for param, btn in self._all_spinboxes.items():
            if self.sender() == btn:
                self._current_values_temp[param] = btn.value()

    def disable_special_ops_tab(self):
        '''
        Disables the content of the special operations tab
        '''
        self.tab_special_ops.setDisabled(True)
        self.label_warning.setVisible(True)

    def enable_special_ops_tab(self):
        '''
        Enables the content of the special operations tab
        '''
        self.tab_special_ops.setEnabled(True)
