"""
Fuzzying test -
Mariusz Suchenek <msuchenek@camk.edu.pl>
reported by Angelo Gargantini
"""

import random
import string
from . import ESP32Alarm, ESP32Warning


class FuzzingESP32:
    def __init__(self, config):
        self.get_all_fields = config["get_all_fields"]

        self.cnt = 0

    def set(self, name, value):
        """
        Set command wrapper
        arguments:
        - name           the parameter name as a string
        - value          the value to assign to the variable as any type
                         convertible to string
        returns: an "OK" string in case of success.
        """

        print("ESP32Serial-DEBUG: set %s %s" % (name, value))

    def set_watchdog(self):
        """
        Set the watchdog polling command

        returns: an "OK" string in case of success.
        """

        return self.set("watchdog_reset", 1)

    def get(self, name):
        """
        Get command wrapper

        arguments:
        - name           the parameter name as a string

        returns: the requested value
        """

        print("ESP32Serial-DEBUG: get %s" % name)

        if name == "pressure":
            value = random.uniform(-1500, 1500)
        elif name == "flow":
            value = random.uniform(-1500, 1500)
        elif name == "battery_charge":
            value = random.uniform(-100, 100)
        elif name == "tidal":
            value = random.uniform(-1500, 1500)
        elif name == "peep":
            value = random.uniform(-100, 100)
        elif name == "temperature":
            value = random.uniform(-100, 100)
        elif name == "battery_powered":
            value = int(random.uniform(0, 1.5))
        elif name == "bpm":
            value = random.uniform(-100, 100)
        elif name == "o2":
            value = random.uniform(-100, 100)
        elif name == "peak":
            value = random.uniform(-100, 100)
        elif name == "total_inspired_volume":
            value = random.uniform(-100, 100)
        elif name == "total_expired_volume":
            value = random.uniform(-100, 100)
        elif name == "volume_minute":
            value = random.uniform(-100, 100)
        elif name == "run":
            value = '0'
        elif name == "alarm":
            value = '0'
        else:
            value = '0'

        self.cnt += 1
        if self.cnt == 1000:
            self.cnt = 0
            value = ''.join(
                (random.choice(string.ascii_letters + string.digits) for i in range(8)))

        # print(str(self.cnt))
        print(str(value))
        return str(value)

    def get_all(self):
        """
        Get the observables as listed in the get_all_fields internal
        object.

        returns: a dict with member keys as written above and values as
        strings.
        """

        print("ESP32Serial-DEBUG: get all")

        values = [self.get(field) for field in self.get_all_fields]
        return dict(zip(self.get_all_fields, values))

    def get_alarms(self):
        """
        Get the alarms from the ESP32

        returns: a ESP32Alarm instance describing the possible alarms.
        """

        return ESP32Alarm(int(self.get("alarm")))

    def get_warnings(self):
        """
        Get the warnings from the ESP32

        returns: a ESP32Warning instance describing the possible warnings.
        """

        return ESP32Warning(int(self.get("warning")))

    def reset_alarms(self):
        """
        Reset all the raised alarms in ESP32

        returns: an "OK" string in case of success.
        """

        return self.set("alarm", 0)

    def reset_warnings(self):
        """
        Reset all the raised warnings in ESP32

        returns: an "OK" string in case of success.
        """

        return self.set("warning", 0)

    def raise_gui_alarm(self):
        """
        Raises an alarm in ESP32

        arguments:
        - alarm_type      an integer representing the alarm type

        returns: an "OK" string in case of success.
        """

        return self.set("alarm", 1)

    def snooze_hw_alarm(self, alarm_type):
        """
        Function to snooze the corresponding alarm in ESP32

        arguments:
        - alarm_type      an integer representing the alarm type. One and
                          only one.

        returns: an "OK" string in case of success.
        """

        # yes, the ESP sends alarms as binary-coded struct, but the snooze
        # happens by means of the exponent
        bitmap = {1 << x: x for x in range(32)}

        pos = bitmap[alarm_type]
        return self.set("alarm_snooze", pos)

    def snooze_gui_alarm(self):
        """
        Function to snooze the GUI alarm in ESP32

        returns: an "OK" string in case of success.
        """

        return self.set("alarm_snooze", 29)
