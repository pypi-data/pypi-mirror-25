# Modem.py - Hologram Python SDK Modem interface
#
# Author: Hologram <support@hologram.io>
#
# Copyright 2016 - Hologram (Konekt, Inc.)
#
#
# LICENSE: Distributed under the terms of the MIT License
from IModem import IModem
from ModemMode import *
from ...Event import Event

import logging
import os

DEFAULT_CHATSCRIPT_PATH = '/chatscripts/default-script'

class Modem(IModem):

    def __init__(self, device_name='/dev/ttyUSB0', baud_rate='9600',
                 chatscript_file=None, event=Event()):

        super(Modem, self).__init__(device_name=device_name, baud_rate=baud_rate,
                                    event=event)

        if chatscript_file is None:
            # Get the absolute path of the chatscript file.
            chatscript_file = os.path.dirname(__file__) + DEFAULT_CHATSCRIPT_PATH

        self.logger.info('chatscript file: %s', chatscript_file)

        # This serial mode device name/port will always be equivalent to whatever the
        # default port is for the specific modem.
        # PPP mode must be instantiated first before Serial to check for existing PPP
        # sessions. Calling and opening a serial port on the same device with an existing
        # PPP session will cause it to hang.
        self._mode = PPP(device_name=self.device_name, baud_rate=baud_rate,
                         chatscript_file=chatscript_file)
        self._serial_mode = Serial(device_name=self.device_name, event=self.event)
        self.logger.info('Instantiated a %s interface with device name of %s',
                         self.__repr__(), self.device_name)

    def isConnected(self):
        raise NotImplementedError('Must instantiate a Modem type')

    def connect(self):
        raise NotImplementedError('Must instantiate a Modem type')

    def disconnect(self):
        raise NotImplementedError('Must instantiate a Modem type')

    def enableSMS(self):
        return self._serial_mode.enableSMS()

    def disableSMS(self):
        return self._serial_mode.disableSMS()

    def popReceivedSMS(self):
        return self._serial_mode.popReceivedSMS()

    @property
    def localIPAddress(self):
        return self._mode.localIPAddress

    @property
    def remoteIPAddress(self):
        return self._mode.remoteIPAddress

    def get_sim_otp_response(self, command):
        return self._serial_mode.get_sim_otp_response(command)

    # EFFECTS: Returns the Received Signal Strength Indication (RSSI) value of the modem
    @property
    def signal_strength(self):
        return self._serial_mode.signal_strength

    @property
    def modem_id(self):
        return self._serial_mode.modem_id

    @property
    def imsi(self):
        return self._serial_mode.imsi

    @property
    def iccid(self):
        return self._serial_mode.iccid

    @property
    def location(self):
        return self._serial_mode.location

    @property
    def operator(self):
        return self._serial_mode.operator

    @property
    def mode(self):
        return self._mode
