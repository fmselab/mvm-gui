"""
Library to interface with the ESP32
"""

from threading import Lock
import serial  # pySerial
from . import ESP32Alarm, ESP32Warning

__all__ = ("ESP32Serial", "ESP32Exception")


class ESP32Exception(Exception):
    """
    Exception class for decoding and hardware failures.
    """

    def __init__(self, verb=None, line=None, output=None, details=None):
        """
        Contructor

        arguments:
        - verb           the transmit verb = {get, set}
        - line           the line transmitted to ESP32 that is failing
        - output         what the ESP32 is replying
        """

        self.verb = str(verb)
        self.line = str(line)
        self.output = str(output)
        self.details = str(details)

        super(ESP32Exception, self).__init__(
            "ERROR in %s: line: %s; output: %s; details: %s" %
            (self.verb, self.line, self.output, self.details))

def _parse(result):
    """
    Parses the message from ESP32

    arguments:
    - result         what the ESP replied as a binary buffer

    returns the requested value as a string
    """

    check_str, value = result.decode().split('=')
    check_str = check_str.strip()

    if check_str != 'valore':
        raise ESP32Exception("", "", "protocol error: 'valore=' expected")
    return value.strip()


class ESP32Serial:
    """
    Main class for interfacing with the ESP32 via a serial connection.
    """

    def __init__(self, config, **kwargs):
        """
        Contructor

        Opens a serial connection to the MVM ESP32

        arguments:
        - config         the configuration object containing at least the
                         "port" and "get_all_fields" keys

        named arguments:
        - any argument available for the serial.Serial pySerial class
        - baudrate       the preferred baudrate, default 115200
        - terminator     the line terminator, binary encoded, default
                         b'\n'
        - timeout        sets the read() timeout in seconds
        """

        self.lock = Lock()

        self.term = kwargs["terminator"] if "terminator" in kwargs else b'\n'

        self._port = config["port"]
        self._port_kwargs = kwargs
        self.reconnect()

        self.get_all_fields = config["get_all_fields"]


    def reconnect(self):
        """
        Reconnects to the ESP32 serial based on initialized settings.
        """
        try:
            self._close_connection()

            baudrate = self._port_kwargs["baudrate"] if "baudrate" in self._port_kwargs else 115200
            timeout = self._port_kwargs["timeout"] if "timeout" in self._port_kwargs else 1
            self.connection = serial.Serial(port=self._port,
                                            baudrate=baudrate, timeout=timeout,
                                            **self._port_kwargs)
            while self.connection.read():
                pass
        except Exception as exc: # pylint: disable=W0703
            raise ESP32Exception("reconnect", None, None, str(exc))

    def _close_connection(self):
        """
        Closes the connection.
        """

        with self.lock:
            if hasattr(self, "connection"):
                self.connection.close()


    def __del__(self):
        """
        Destructor.

        Closes the connection.
        """

        self._close_connection()

    def _write(self, cmd):
        """
        Writes the un-encoded message to the ESP32.
        The command is stored as the last cmd.

        arguments:
        - cmd           the unencoded command
        """
        result = b""
        try:
            result = self.connection.write(cmd.encode())
        except Exception as exc: # pylint: disable=W0703
            raise ESP32Exception("write", cmd, result.decode(), str(exc))

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

        with self.lock:
            # I know about Python 3.7 magic string formatting capability
            # but I don't really remember now the version running on
            # Raspbian
            command = 'set ' + name + ' ' + str(value) + '\r\n'
            self._write(command)

            result = b""
            try:
                result = self.connection.read_until(terminator=self.term)
                return _parse(result)
            except Exception as exc: # pylint: disable=W0703
                raise ESP32Exception("set", command, result.decode(), str(exc))

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

        with self.lock:
            command = 'get ' + name + '\r\n'
            self._write(command)

            result = b""
            try:
                result = self.connection.read_until(terminator=self.term)
                return _parse(result)
            except Exception as exc: # pylint: disable=W0703
                raise ESP32Exception("get", command, result.decode(), str(exc))

    def get_all(self):
        """
        Get the observables as listed in the get_all_fields internal
        object.

        returns: a dict with member keys as written above and values as
        strings.
        """

        print("ESP32Serial-DEBUG: get all")

        with self.lock:
            self._write("get all\r\n")

            result = b""
            try:
                result = self.connection.read_until(terminator=self.term)
                values = _parse(result).split(',')

                if len(values) != len(self.get_all_fields):
                    raise Exception("get_all answer mismatch: expected: %s, got %s" % (
                        self.get_all_fields, values))

                return dict(zip(self.get_all_fields, values))
            except Exception as exc: # pylint: disable=W0703
                raise ESP32Exception("get", "get all", result.decode(), str(exc))

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

    def venturi_calibration(self):
        """
        Generator function to retrieve data for spirometer calibration.

        returns a helper class instance.
        """

        class VenturiRetriever():
            """
            Helper class to wrap all the complexity and problems raising
            from the protocol used to retrieve the Venturi Calibration
            data.
            """

            def __init__(self, esp32):
                """
                Constructor

                arguments:
                - esp32: an istance of ESP32Serial
                """

                self._esp32 = esp32

                self._esp32.set("flush_pipe", 1)

                # from this point, the class effectively OWNS the
                # connection...

                self._esp32.lock.acquire()

                self._previous_timeout = self._esp32.connection.timeout
                self._esp32.connection.timeout = 2
                self._esp32.connection.write("get venturi_scan\r\n".encode())

            def data(self):
                """
                This function is a generator. It yields data as they come
                out and returns when the work is finished.

                Use it like:

                ```
                for data in data():
                    #work on a chunk of data
                ```

                yields a list of (3) floats:
                1. measure index (percentage)
                2. raw measured flow (spirometer)
                3. pressure variation (Sinsirion)
                """

                while True:
                    bresult = self._esp32.connection.read_until(
                        terminator=self._esp32.term)

                    result = bresult.decode().strip()
                    if result == '':
                        raise ESP32Exception("get", "get venturi_scan", "timeout")
                    elif result == 'valore=OK':
                        return
                    yield [float(datum) for datum in result.split(',')]

            def __del__(self):
                """
                Destructor

                this puts the connection back in normal operation
                """

                # read any possibly remaining data.
                # For example if the generator has not been called till
                # the end of the procedure.
                while self._esp32.connection.read():
                    pass
                # restore the timeout to the previously using value
                self._esp32.connection.timeout = self._previous_timeout
                self._esp32.lock.release()
                # ...and from here it finally releases its ownership
                self._esp32.set("flush_pipe", 0)

        return VenturiRetriever(self)

    def leakage_test(self):
        """
        Generator function to retrieve data for leakage test.

        returns a helper class instance.
        """

        class LeakTestRetriever():
            """
            Helper class to wrap all the complexity and problems raising
            from the protocol used to retrieve the leakage test data.
            """

            def __init__(self, esp32):
                """
                Constructor

                arguments:
                - esp32: an istance of ESP32Serial
                """

                self._esp32 = esp32

                # from this point, the class effectively OWNS the
                # connection...

                self._esp32.lock.acquire()

                self._previous_timeout = self._esp32.connection.timeout
                self._esp32.connection.timeout = 2
                self._esp32.connection.write("get leakage_test\r\n".encode())

            def data(self):
                """
                This function is a generator. It yields data as they come
                out and returns when the work is finished.

                Use it like:

                ```
                for data in data():
                    #work on a chunk of data
                ```

                yields a list of (3) floats:
                1. completed percentage
                2. internal pressure
                3. pressure at the patient mouth
                """

                while True:
                    bresult = self._esp32.connection.read_until(
                        terminator=self._esp32.term)

                    result = bresult.decode().strip()
                    if result == '':
                        raise ESP32Exception("get", "get leakage_test", "timeout")
                    elif result == 'valore=OK':
                        return
                    yield [float(datum) for datum in result.split(',')]

            def __del__(self):
                """
                Destructor

                this puts the connection back in normal operation
                """

                # read any possibly remaining data.
                # For example if the generator has not been called till
                # the end of the procedure.
                while self._esp32.connection.read():
                    pass
                # restore the timeout to the previously using value
                self._esp32.connection.timeout = self._previous_timeout
                self._esp32.lock.release()
                # ...and from here it finally releases its ownership

        return LeakTestRetriever(self)
