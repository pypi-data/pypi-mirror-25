"""
MODULE:       serialreader
PURPOSE:      get the data from the serial console and store it in the
              data store.
AUTHOR(S):    michael lustenberger inofix.ch
COPYRIGHT:    (C) 2017 by Michael Lustenberger and INOFIX GmbH

              This program is free software under the GNU General Public
              License (v3).
"""

import json
import serial
import threading
from time import sleep

class SerialReader(threading.Thread):
    """
    Reader class for connecting to an end device and reading its output
    """

    def __init__(self, device, baudrate, store, rounds=100, timeout=60):
        """
        Initialize the serial reader class
            device        device name to connect to
            baudrate      the baud rate for the serial line
            store        the data store object to send the data to
            rounds        number of rounds to run / listen for input
        """
        threading.Thread.__init__(self)
        self.baudrate = baudrate
        self.store = store
        self.rounds = rounds
        self.do_run = True
        self.device_name = device
        try:
            if device:
                self.device = serial.Serial(device, self.baudrate, timeout=timeout);
        except serial.serialutil.SerialException:
            print("Could not connect to the serial line at " + self.device_name)

    def age(self):
        """
        Get closer to your EOL
        """
        # 0 means this composer will never decompose
        if self.rounds == 1:
            self.do_run = False
        elif self.rounds > 1:
            self.rounds -= 1

    def run(self):
        """
        Open a connection over the serial line and receive data lines
        """
        if not self.device:
            return
        try:
            data = ""
            while (self.do_run):
                try:
                    if (self.device.inWaiting() > 1):
                        l = self.device.readline()[:-2]
                        l = l.decode("UTF-8")

                        if (l == "["):
                            # start recording
                            data = "["
                        elif (l == "]") and (len(data) > 4) and (data[0] == "["):
                            # now parse the input
                            data = data + "]"
                            self.store.register_json(data)
                            self.age()
                        elif (l[0:3] == "  {"):
                            # this is a data line
                            data = data + " " + l
                    else:
                        # this is a slow interface - give it some time
                        sleep(1)
                        # then count down..
                        self.age()
                except (UnicodeDecodeError, ValueError):
                    # only accepting unicode: throw away the whole bunch
                    data = ""
                    # and count down the exit condition
                    self.age()

        except serial.serialutil.SerialException:
            print("Could not connect to the serial line at " + self.device_name)

    def halt(self):
        """
        Tell the this object to stop working after the next round
        """
        self.do_run = False


