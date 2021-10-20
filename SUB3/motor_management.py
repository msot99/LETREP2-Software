import serial
from time import sleep
import threading
BAUD = 115200

class motor:
    def __init__(self, com, max, min):
        self.com = com
        self.ser = serial.Serial(com, BAUD, timeout=.1)
        self.preload_max = max
        self.preload_min = min
        self.torque_update = False
        self.torque = 0
        self.torque_thread = None

    def enable(self):
        self.ser.write("a".encode())
        #TODO Add ack checks
    

    def torque(self):
        print("A")
        # print(self.read_torque)
        # while(self.read_torque):
        #     data_from_ser = self.ser.readline().decode()
        #     print(data_from_ser)

    # This function stops all processes and disables motor
    def stop(self):
        self.ser.write("d".encode())
        #TODO Add ack checks
        
        #Stop the torque input thread
        if self.torque_thread:
            self.read_torque = False
            self.torque_thread.join()
    
    # This function starts the torque capturing process
    def start_torque_readings(self):
        self.read_torque = True
    
        torque_thread = threading.Thread(target=self.torque)
        sleep(1)
        # print(self.torque_thread.is_alive())
        torque_thread.start()
        print(torque_thread.is_alive())
   








def main():
    mot = motor("COM15", .51,.53)
    mot.enable()
    mot.start_torque_readings() 
    sleep(10)
    mot.stop()




if __name__ == "__main__":
    main()
