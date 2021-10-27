import serial
import time
from time import sleep
from threading import Thread
import random
from emg import SAMPLES_TO_COLLECT, emg
from block import block
from trial import trial

# Constants
PRELOAD_DEBOUCE_TIME = .5
BAUD = 115200
SAMPLES_TO_COLLECT = 2000


class motor:
    def __init__(self, com):
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
        self.ser.write("a".encode())
        # TODO Add ack checks

    def disable(self):
        """
        Sends disable command to the ESP32 to disable to clearpath motor
        """
        self.ser.write("d".encode())
        # TODO Add ack checks

    def fire(self):
        """
        Sends fire command to the ESP32 to actuate the clearpath motor to the raised position
        """
        self.ser.write("b".encode())
        # TODO Add ack checks

    def release(self):
        """
        Sends release command to the ESP32 to return the clearpath motor to starting position
        """
        self.ser.write("c".encode())
        # TODO Add ack checks

    def _read_msgs_from_esp(self):
        """
        Processes the next command and updates the torque value
        """
        while(self._read_msgs_flag):
            data_from_ser = self.ser.readline().decode().strip()
            if data_from_ser[:3] == "TOR":
                self.torque_value = float(data_from_ser.split(':')[1])
                self.torque_update = True



    def _take_trial(self):
        """This function completes a full trial"""
        # Variables for tracking how long to wait before firing
        good_torque_start_time = time.time()
        time_needed_to_fire = 2.0 + random.random() * MAX_PRELOAD_LENGTH
        print("GOOD TORQUE! Waiting %d seconds before fire" %
              time_needed_to_fire)
        while(True):
            sleep(.1)
            #  Check to see if we are in paused mode,
            # If so do not fire torque
            if self.pause_fire:
                print("Paused-leaving preload for fire")
                return

            # Check to see if patient is maintaining torque window
            if not(self._preload_min < self.torque_value and self._preload_max > self.torque_value):

                if self._preload_min > self.torque_value:
                    if time.time() - good_torque_start_time > PRELOAD_DEBOUCE_TIME:
                        print("PRELOAD_FAILURE LOW")
                        break
                else:
                    if time.time() - good_torque_start_time > PRELOAD_DEBOUCE_TIME:

                        print("PRELOAD_FAILURE HIGH")
                        break
                # TODO Add communication for preload failure
                if time.time() - good_torque_start_time < PRELOAD_DEBOUCE_TIME:
                    print("Failed Preload, but in debounce")

    def _fire_motor_on_torque(self):
        """
        Handles when the system fires the motor 
        """
        while(self._fire_motor_flag):
            sleep(.1)
            if self._preload_min < self.torque_value and self._preload_max > self.torque_value and not self.pause_fire:

                 # Fire the motor after specified period
                if time.time() - good_torque_start_time > time_needed_to_fire:
                    self.emg.emg_trig_collection(
                        self.emg_data_array, SAMPLES_TO_COLLECT)
                    print("FIRE!!")
                    self._fire()
                    sleep(.5)
                    self._release()

        print("Stopped motor fire")

    def torque_preload_good(self):
        if self.torque > self.preload_max:
            return 1
        elif self.torque < self.preload_min:
            return -1
        else:
            return 0
    def start(self):
        """
        Starts the system's threads and enables the motor
        """
        self._start_threads()
        sleep(.1)
        self._enable()

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
        self._disable()

        # Stop the motor input thread
        if self._motor_thread:
            self._fire_motor_flag = False
            self._motor_thread.join()

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
        # Create Threads
        self._comm_thread = Thread(target=self._read_msgs_from_esp)
        self._motor_thread = Thread(target=self._fire_motor_on_torque)

        # Start Threads
        self._comm_thread.start()
        self._motor_thread.start()


def main():
    mot = motor("COM15", .53, .51)
    mot.start()
    sleep(3)
    mot.exit()


if __name__ == "__main__":
    main()
