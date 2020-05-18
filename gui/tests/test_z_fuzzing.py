# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
import threading
from .mvm_basics import *
from mainwindow import MainWindow
from messagebox import MessageBox
from start_stop_worker import StartStopWorker
from PyQt5.QtCore import QCoreApplication
from communication.fuzzing_esp32 import FuzzingESP32
from communication.fake_esp32serial import FakeESP32Serial
from PyQt5.Qt import QTimer
from _pytest.outcomes import fail


MIN_TIME_WITHOUT_CRASHING_MS = 20000

"""
try the main windows for a min amount of time with some invalid data
and check that it does not crashes
"""
def start_simulate(_qtbot,esp32):        
    '''
    '''
    assert qt_api.QApplication.instance() is not None

    assert config is not None

    window = MainWindow(config, esp32)
    _qtbot.addWidget(window)
    window.show()
    # press new patient
    _qtbot.mouseClick(window.button_new_patient,QtCore.Qt.LeftButton)
    # press proceed
    _qtbot.mouseClick(window.button_start_vent,QtCore.Qt.LeftButton)
    # TODO check that the main window has started
    assert True
    #
    def finish():
        window.close()
    # wait for some time
    timer = QTimer
    # MIN_TIME_WITHOUT_CRASHING_MS without crashing
    timer.singleShot(MIN_TIME_WITHOUT_CRASHING_MS,finish)
    # wait until has finished - or fail if crashes
    _qtbot.waitUntil(lambda: not window.isVisible(), timeout=MIN_TIME_WITHOUT_CRASHING_MS+1000)
    # if it exits because it has been closed -> pass
    # it it exits because it reaches the timeout -> it fails

"""
fuzzing test. try the main windows for a min amount of time with some invalid data
and check that it does not crash
"""
def test_start_fuzzing(qtbot):
    start_simulate(qtbot,FuzzingESP32(config))

"""
test w fake esp32. try the main windows for a min amount of time with some valid data from the fake 32
and check that it does not crash
"""
# def test_start_fakeESP32(qtbot):
#     esp32 = FakeESP32Serial(config)
#     start_simulate(qtbot, esp32)

