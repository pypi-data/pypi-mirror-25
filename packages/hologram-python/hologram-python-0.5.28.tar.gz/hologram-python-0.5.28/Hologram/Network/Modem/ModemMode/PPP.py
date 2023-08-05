# PPP.py - Hologram Python SDK Modem PPP interface
#
# Author: Hologram <support@hologram.io>
#
# Copyright 2016 - Hologram (Konekt, Inc.)
#
#
# LICENSE: Distributed under the terms of the MIT License
#
import subprocess
import sys
import time
from pppd import PPPConnection
from IPPP import IPPP
from Exceptions.HologramError import PPPError

DEFAULT_PPP_TIMEOUT = 200
DEFAULT_PPP_INTERFACE = 'ppp0'
MAX_PPP_INTERFACE_UP_RETRIES = 10
MAX_REROUTE_PACKET_RETRIES = 15

class PPP(IPPP):

    def __init__(self, device_name='/dev/ttyUSB0', baud_rate='9600',
                 chatscript_file=None):


        super(PPP, self).__init__(device_name=device_name, baud_rate=baud_rate,
                                  chatscript_file=chatscript_file)

        try:
            self.__enforce_no_existing_ppp_session()
        except PPPError as e:
            self.logger.error(repr(e))
            sys.exit(1)

        self._ppp = PPPConnection(self.device_name, self.baud_rate, 'noipdefault',
                                  'usepeerdns', 'defaultroute', 'persist', 'noauth',
                                  connect=self.connect_script)

    def isConnected(self):
        return self._ppp.connected()

    # EFFECTS: Establishes a PPP connection. If this is successful, it will also
    #          reroute packets to ppp0 interface.
    def connect(self, timeout=DEFAULT_PPP_TIMEOUT):

        try:
            self.__enforce_no_existing_ppp_session()
        except PPPError as e:
            self.logger.error(repr(e))
            sys.exit(1)

        result = self._ppp.connect(timeout=timeout)

        if result == True and self.__is_ppp_interface_up():
            self.__reroute_packets()
            return True
        else:
            return False

    def disconnect(self):
        self.__shut_down_existing_ppp_session()
        return self._ppp.disconnect()

    # EFFECTS: Blocks to make sure ppp interface is up.
    def __is_ppp_interface_up(self):
        count = 0
        while count <= MAX_PPP_INTERFACE_UP_RETRIES:
            try:
                out_list = subprocess.check_output(['ip', 'address', 'show', 'dev',
                                                    DEFAULT_PPP_INTERFACE],
                                                   stderr=subprocess.STDOUT)

                # Check if ready to break out of loop when ppp0 is found.
                if 'does not exist' in out_list:
                    time.sleep(1)
                    count += 1
                else:
                    break
            except subprocess.CalledProcessError as e:
                pass

        if count <= MAX_PPP_INTERFACE_UP_RETRIES:
            return True
        return False

    # EFFECTS: Makes sure that there are no existing PPP instances on the same
    #          device interface.
    def __enforce_no_existing_ppp_session(self):

        process = self.__check_for_existing_ppp_sessions()

        if process is None:
            return

        pid = self.__split_PID_from_process(process)
        if pid is not None:
            raise PPPError('An existing PPP session established by pid %s is currently using the %s device interface. Please close/kill that process first'
                             % (pid, self.device_name))

    def __shut_down_existing_ppp_session(self):
        process = self.__check_for_existing_ppp_sessions()

        if process is None:
            return

        pid = self.__split_PID_from_process(process)

        # Process this only if it is a valid PID integer.
        if pid is not None:
            kill_command = 'kill ' + str(pid)
            self.logger.info('Killing pid %s that currently have an active PPP session',
                             pid)
            subprocess.call(kill_command, shell=True)

    def __check_for_existing_ppp_sessions(self):
        self.logger.info('Checking for existing PPP sessions')
        out_list = subprocess.check_output(['ps', '--no-headers', '-axo',
                                            'pid,user,tty,args']).split('\n')

        # Get the end device name, ie. /dev/ttyUSB0 becomes ttyUSB0
        temp_device_name = self.device_name.split('/')[-1]

        # Iterate over all processes and find pppd with the specific device name we're using.
        for process in out_list:
            if 'pppd' in process and temp_device_name in process:
                self.logger.info('Found existing PPP session on %s', temp_device_name)
                return process

        return None

    # REQUIRES: A string process
    # EFFECTS: Returns the pid in integer form, None otherwise.
    def __split_PID_from_process(self, process):
        processList = process.split(' ')

        # iterate through the list and return the pid. PID should always come out
        # in front.
        for x in processList:
            if x.isdigit():
                return int(x)

        return None

    def __reroute_packets(self):
        self.logger.info('Rerouting packets to %s interface', DEFAULT_PPP_INTERFACE)

        count = 0
        # Make sure that we still have ppp interface before adding the routes.
        while count <= MAX_REROUTE_PACKET_RETRIES:
            try:
                out_list = subprocess.check_output(['ip', 'route', 'add',
                                                    '10.176.0.0/16', 'dev',
                                                    DEFAULT_PPP_INTERFACE],
                                                   stderr=subprocess.STDOUT)

                # Check if ready to break out of loop when ppp0 is found.
                if 'Network is down' in out_list:
                    time.sleep(1)
                    count += 1
                else:
                    break
            except Exception as e:
                pass

        if count > MAX_REROUTE_PACKET_RETRIES:
            return

        subprocess.call('ip route add 10.254.0.0/16 dev %s' % DEFAULT_PPP_INTERFACE, shell=True)
        subprocess.call('ip route add default dev %s' % DEFAULT_PPP_INTERFACE, shell=True)

    @property
    def localIPAddress(self):
        return self._ppp.raddr

    @property
    def remoteIPAddress(self):
        return self._ppp.laddr
