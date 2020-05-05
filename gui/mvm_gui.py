#!/usr/bin/env python3
'''
Runs the MVM GUI
'''

import sys
import os
import os.path
from PyQt5 import QtCore, QtWidgets
from serial import SerialException

import yaml

from mainwindow import MainWindow
from exception_wrapper import ExceptionWrapper
from communication.esp32serial import ESP32Serial, ESP32Exception
from communication.fake_esp32serial import FakeESP32Serial
from messagebox import MessageBox


def connect_esp32(config):
    """
    Establish a serial connection with the ESP32.

    arguments:
    - config: a dictionary like representing the program configuration.

    returns: a valid ESP32Serial object if connection has been
    established, a FakeESP32Serial object if has been requested to run the
    software mockup, 'None' on error.
    """

    try:
        if 'fakeESP32' in sys.argv:
            err_msg = "Cannot setup FakeESP32Serial"
            print('******* Simulating communication with ESP32')
            raw_esp32 = FakeESP32Serial(config)
        else:
            err_msg = "Cannot communicate with port %s" % config['port']
            raw_esp32 = ESP32Serial(config)

    except SerialException as error:
        msg = MessageBox()
        answer = msg.critical("Do you want to retry?",
                              "Severe hardware communication error",
                              str(error) + err_msg, "Communication error",
                              {msg.Retry: lambda: connect_esp32(config),
                               msg.Abort: lambda: None})
        return answer()

    return raw_esp32

def main():
    """
    Main function.
    """
    app = QtWidgets.QApplication(sys.argv)

    base_dir = os.path.dirname(__file__)
    settings_file = os.path.join(base_dir, 'default_settings.yaml')

    with open(settings_file) as fsettings:
        config = yaml.load(fsettings, Loader=yaml.FullLoader)
    print('Config:', yaml.dump(config), sep='\n')

    # Initialize ESP32 connection
    raw_esp32 = connect_esp32(config)
    if raw_esp32 is None:
        sys.exit(-1)

    # Wrap the raw ESP32 class in an Exception Wrapper
    esp32 = ExceptionWrapper(raw_esp32, ESP32Exception)

    # Spawn mainwindow
    window = MainWindow(config, esp32)
    window.show()

    # Assign exception function
    esp32.assign_except_func(window.critical_alarm_handler.call_communication_failure)

    # Set up watchdog and star the main Qt executable
    esp32.set("wdenable", 1)
    watchdog = QtCore.QTimer()
    def watchdog_redirect():
        try: esp32.set_watchdog()
        except ESP32Exception: return
    watchdog.timeout.connect(watchdog_redirect)
    watchdog.start(config["wdinterval"] * 1000)
    app.exec_()
    esp32.set("wdenable", 0)


if __name__ == "__main__":
    main()
