import serial
import time
from time import sleep
from threading import Thread
import random

# Constants
PRELOAD_DEBOUCE_TIME = .5
BAUD = 115200

class motor:
    def __init__(self, com,max,min):
        # Serial for communication with ESP32
        self.ser = serial.Serial(com, BAUD, timeout=.1)

        self._comm_thread = None

        # Values for preload
        self._preload_max = max
        self._preload_min = min

        # Flags for communcation/messaging thread
        self._read_msgs_flag = True

        # Flags for controlling motor
        self._fire_motor_flag = True

        # Public variables for interfacing
        self.torque_update = False
        self.torque_value = 0
        self.pause_fire = True

    def enable(self):
        """
        Sends enable command to the ESP32 to enable to clearpath motor
        """
        print("Enabling Motor")
        self.ser.write("a".encode())
        # TODO Add ack checks

    def disable(self):
        """
        Sends disable command to the ESP32 to disable to clearpath motor
        """
        print("Disabling Motor")
        self.ser.write("d".encode())
        # TODO Add ack checks

    def fire(self):
        """
        Sends fire command to the ESP32 to actuate the clearpath motor to the raised position
        """
        print("Firing Motor")
        self.ser.write("b".encode())
        # TODO Add ack checks

    def release(self):
        """
        Sends release command to the ESP32 to return the clearpath motor to starting position
        """
        print("Releasing Motor")
        self.ser.write("c".encode())
        # TODO Add ack checks

    def _read_msgs_from_esp(self):
        """
        Processes the next command and updates the torque value
        """
        while(self._read_msgs_flag):
            if self.ser.in_waiting > 0:
                try:
                    data_from_ser = self.ser.readline().decode().strip()
                except UnicodeDecodeError:
                    print("thread go oopsies")
                if data_from_ser[:3] == "TOR":
                    self.torque_value = float(data_from_ser.split(':')[1])
                    self.torque_update = True
                # else:

                    # print(data_from_ser)
            sleep(.01)

    def torque_preload_check(self):
        """
        Checks the motors torque:
        Returns 1 if greater than preload_max
        Return 0 if good
        Returens -1 if less than preload_min
        """
        # print(self.torque_value, self._preload_min, self._preload_max)
        if self.torque_value > self._preload_max:
            return 1
        elif self.torque_value < self._preload_min:
            return -1
        else:
            return 0

    def start(self):
        """
        Starts the system's threads and enables the motor
        """
        self._start_threads()
        sleep(.1)
        self.enable()

    def play_pause(self):
        """"
        Pauses the motor firing ability until turned back on
        """
        self.pause_fire = not self.pause_fire

    def exit(self):
        """
        Closes serial stops all threads and disables the motor
        """
        # Turn off motor
        print("Motor is exiting")
        self.disable()
        sleep(4)

        # Stop comm thread
        if self._comm_thread:
            self._read_msgs_flag = False
            self._comm_thread.join()

        # Close the serial
        if self.ser:
            self.ser.close()

    def _start_threads(self):
        """
        starts threads for serial and system firing
        """
        # Create Thread(s)
        self._comm_thread = Thread(target=self._read_msgs_from_esp)

        # Start Thread(s)
        self._comm_thread.start()


def main():
    mot = motor("COM15", .53, .51)
    mot.start()
    sleep(3)
    mot.exit()


if __name__ == "__main__":
    main()
