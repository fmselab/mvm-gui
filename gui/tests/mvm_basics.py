import os, yaml

from communication.fake_esp32serial import FakeESP32Serial
from alarm_handler import AlarmHandler
from PyQt5 import QtCore, QtGui, QtWidgets

base_dir = os.environ['MVMGUI_BASEDIR']
settings_file = os.path.join(base_dir, 'gui/default_settings.yaml')
with open(settings_file) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)



def wrongConfigurationFile():
    base_dir = os.environ['MVMGUI_BASEDIR']
    settings_file = os.path.join(base_dir, 'gui/default_settings2.yaml')
    with open(settings_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)