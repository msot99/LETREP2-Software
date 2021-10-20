import serial
BAUD = 115200

class motor:
    def __init__(self,com):
        self.com = com
        self.ser = serial.Serial(com, BAUD, timeout=.1)
    
    def communicator(self):
        self.ser.write("a".encode())
        while(True):
            
            data_from_esp = self.ser.readline().decode().strip()
            print("READ",data_from_esp)
            if data_from_esp[0:4]=="TOR":
                torque = float(data_from_esp.split(":")[1])
                print(torque)












def main():
    mot = motor("COM15")
    mot.communicator()



if __name__ == "__main__":
    main()
