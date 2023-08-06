# MockSerial.py - Hologram Python SDK Modem Mock Serial interface
#
# Author: Hologram <support@hologram.io>
#
# Copyright 2016 - Hologram (Konekt, Inc.)
#
#
# LICENSE: Distributed under the terms of the MIT License
#
from ISerial import ISerial
from UtilClasses import ModemResult

DEFAULT_SERIAL_DEVICE_NAME = '/dev/ttyACM1'
DEFAULT_SERIAL_BAUD_RATE = 9600

class MockSerial(ISerial):

    def __init__(self, device_name=DEFAULT_SERIAL_DEVICE_NAME,
                 baud_rate=DEFAULT_SERIAL_BAUD_RATE, timeout=1):
        super(MockSerial, self).__init__(device_name=device_name,
                                     baud_rate=DEFAULT_SERIAL_BAUD_RATE,
                                     timeout=timeout)

    def openSerialPort(self, device_name=DEFAULT_SERIAL_DEVICE_NAME,
                       baud_rate=DEFAULT_SERIAL_BAUD_RATE, timeout=1):
        return True

    def closeSerialPort(self):
        pass

    # This is used to simulate the internal serial buffer.
    def setSerialBuffer(self, buff):
        self._serial_port_buffer = buff

    def getSerialBuffer(self):
        return self._serial_port_buffer

    def write(self, msg):
        response = 'AT' + msg + '\r\r\n' + msg + ': 1234567890123456789\r\n\r\nOK\r\n'
        return response

    def _read(self, timeout=None, size=ISerial.DEFAULT_SERIAL_READ_SIZE):
        response = '1234567890123456789\r\n\r\nOK\r\n'
        return response

    def readline(self, timeout=None):
        return self.serial_port

    def command(self, cmd='', value=None, expected=None, timeout=None, retries=1,
                seteq=False, read=False, prompt=None, data=None):
        self.result = ModemResult.OK
        self._commandResult()

    def set(self, cmd, value, expected=None, timeout=None,
            retries=1, prompt=None, data=None):
        pass
