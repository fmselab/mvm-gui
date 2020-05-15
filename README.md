# MVM - gui

## Code organization

- the `gui` folder is deputed to contain the Python files for the GUI
- the `mock` folder contains the mock-ups for testing purposes, basically
  to mimic hardware interaction

## Requirements

- Python >= 3.5 (but not 3.8 because PyQtGraph is [incompatible](https://github.com/conda-forge/pyqtgraph-feedstock/issues/10))
- RPi.GPIO
- PyQt5
- PyQtGraph
- PySerial
- PyYaml
- numpy

## Fonts
The following fonts have to be present to obtain consistent look
- [Noto Mono](https://www.google.com/get/noto/#mono-mono)
- [Cantarell](https://fonts.google.com/specimen/Cantarell)

# Run

You can run with:
```
cd gui/
./mvm_gui.py
```
By default, the program will read from the specified serial port.

## Test
If you want to run with simulated input, the program is invoked with:
```
./mvm_gui.py fakeESP32
```

In the fuzzy testing mode, activated by the following command:
```
./mvm_gui.py fuzzingESP32
```
the input is simulated adding random errors.

## Settings
Default settings are stored in:
```
./gui/default_settings.yaml
```

Basics settings are:
- port: (string) the serial port to use

More settings and description can be found in the yaml file itself.

If you want to read from an Arduino (ESP), you need to upload `mock/mock.ino`
to your Arduino device, and specify the serial port in the settings file.
