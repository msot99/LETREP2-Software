import serial
import time
from time import sleep
from threading import Thread
import random

# Constants
MIN_PRELOAD_LENGTH = 2
MAX_PRELOAD_LENGTH = 8
BAUD = 115200

class motor:
    def __init__(self, com, max, min):
        # Serial for communication with ESP32
        self.ser = serial.Serial(com, BAUD, timeout=.1)
        
        self._comm_thread = None
        self._motor_thread = None

        # Values for preload
        self._preload_max = max
        self._preload_min = min

        # Flags for communcation/messaging thread
        self._read_msgs_flag = True
        self.torque_update = False

        self.torque_value = 0

        # Flags for controlling motor
        self._fire_motor_flag = True
        self._pause_fire = True

    def _enable(self):
        """
        Sends enable command to the ESP32 to enable to clearpath motor
        """
        self.ser.write("a".encode())
        #TODO Add ack checks
    
    def _disable(self):
        """
        Sends disable command to the ESP32 to disable to clearpath motor
        """
        self.ser.write("d".encode())
        #TODO Add ack checks
    
    def _fire(self):
        """
        Sends fire command to the ESP32 to actuate the clearpath motor to the raised position
        """
        self.ser.write("b".encode())
        #TODO Add ack checks

    def _release(self):
        """
        Sends release command to the ESP32 to return the clearpath motor to starting position
        """
        self.ser.write("c".encode())
        #TODO Add ack checks
    
    def _read_msgs_from_esp(self):
        """
        processes the next command and updates the torque value
        """
        while(self._read_msgs_flag):
            data_from_ser = self.ser.readline().decode().strip()
            if data_from_ser[:3] == "TOR":
                self.torque_value = float(data_from_ser.split(':')[1])
                self.torque_update = True
                
            if data_from_ser == "enabled":
                sleep(2)
                self._pause_fire = False

    def _fire_motor_on_torque(self):
        """
        handles when the system fires the motor 
        """
        while(self._fire_motor_flag):
            sleep(.1)
            if self._preload_min < self.torque_value and self._preload_max > self.torque_value and not self._pause_fire:
                # Variables for tracking how long to wait before firing
                good_torque_start_time = time.time()
                time_needed_to_fire = random.randint(
                    MIN_PRELOAD_LENGTH, MAX_PRELOAD_LENGTH)
                print("GOOD TORQUE! Waiting %d seconds before fire" % time_needed_to_fire)
                while(True):
                    sleep(.1)
                    #  Check to see if we are in paused mode,
                    # If so do not fire torque
                    if self._pause_fire:
                        print("Paused-leaving preload for fire")
                        break

                    # Check to see if patient is maintainging torque window
                    if not(self._preload_min < self.torque_value and self._preload_max > self.torque_value):
                        print("PRELOAD_FAILURE")
                        # TODO Add communication for preload failure
                        break

                    # Fire the motor after specified period
                    if time.time() - good_torque_start_time > time_needed_to_fire:
                        # TODO Add communication for fired
                        print("FIRE!!")
                        self._fire()
                        sleep(.5)
                        self._release()
                        sleep(1)
                        break
        
        print("Stopped motor fire")

    def start(self):
        """
        starts the system's threads and enables the motor
        """
        self._start_threads()
        sleep(.1)
        self._enable()
        

    def play_pause(self):
        """"
        Pauses the motor firing ability until turned back on
        """
        self._pause_fire = not self._pause_fire
        

    def exit(self):
        """
        closes serial stops all threads and disables the motor
        """
        # Turn off motor
        self._disable()

        #Stop the motor input thread
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
    mot = motor("COM15", .53,.51)
    mot.start()
    sleep(3)
    mot.exit()




if __name__ == "__main__":
    main()
