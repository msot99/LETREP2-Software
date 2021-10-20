from collections import deque
import threading
from DataManager import DataKernel
import clr
from time import sleep
clr.AddReference("/resources/DelsysAPI")
clr.AddReference("System.Collections")

from Aero import AeroPy
from System.Collections.Generic import List
from System import Int32

key = "MIIBKjCB4wYHKoZIzj0CATCB1wIBATAsBgcqhkjOPQEBAiEA/////wAAAAEAAAAAAAAAAAAAAAD///////////////8wWwQg/////wAAAAEAAAAAAAAAAAAAAAD///////////////wEIFrGNdiqOpPns+u9VXaYhrxlHQawzFOw9jvOPD4n0mBLAxUAxJ02CIbnBJNqZnjhE50mt4GffpAEIQNrF9Hy4SxCR/i85uVjpEDydwN9gS3rM6D0oTlF2JjClgIhAP////8AAAAA//////////+85vqtpxeehPO5ysL8YyVRAgEBA0IABKtktl6PHswln5DTRdPbDJtbDN+KTpbIjfcmBQeGmBRqq/61zfuFgaRVuOTNbPm4rDTHnbap/KzNttIofOzAOLs="
license = "<License>"\
          "<Id>9f6b5edf-19ab-45a2-aa33-acb8d5f1fbfc</Id>"\
          "<Type>Standard</Type>"\
          "<Quantity>10</Quantity>"\
          "<LicenseAttributes>"\
          "<Attribute name=\"Software\">VS2012</Attribute>"\
          "</LicenseAttributes>"\
          "<ProductFeatures>"\
          "<Feature name=\"Sales\">True</Feature>"\
          "<Feature name=\"Billing\">False</Feature>"\
          "</ProductFeatures>"\
          "<Customer>"\
          "<Name>Kotaro Sasaki</Name>"\
          "<Email>KoSasaki@letu.edu</Email>"\
          "</Customer>"\
          "<Expiration>Wed, 01 Jan 2031 05:00:00 GMT</Expiration>"\
          "<Signature>MEYCIQCo6q0QdGF6/Yx8SNk23u+XBSvAoqWTPsrLU2YZqzHT+wIhAOgzi0LuVav4wj/JH3wNXI7uMz/98/bydSm4IKtnePoV</Signature>"\
          "</License>"


class TrignoBase():
    def __init__(self):
        self.BaseInstance = AeroPy()


class emg:
    def __init__(self, array):
        self.array_to_store = array
        self.packetCount = 0
        self.pauseFlag = False
        self.numSamples = 10000
        base = TrignoBase()
        self.TrigBase = base.BaseInstance
        self.DataHandler = DataKernel(self.TrigBase)
    
    def Connect(self):
        """Callback to connect to the base"""
        self.TrigBase.ValidateBase(key, license, "RF")


    def streaming(self):
        """This is the data processing thread"""
        self.emg_queue = deque()
        
        
        while self.pauseFlag is False:
            dataReady = self.TrigBase.CheckDataQueue()
            if dataReady:
                DataOut = self.TrigBase.PollData()
                
                self.array_to_store.extend([abs(i) for i in DataOut[0][0] if abs(i)<3])

        print(self.DataHandler.getPacketCount())

    def Start(self):
        """Callback to start the data stream from Sensors"""

        self.pauseFlag = False
        newTransform = self.TrigBase.CreateTransform("raw")
        index = List[Int32]()

        self.TrigBase.ClearSensorList()

        for i in range(self.SensorsFound):
            selectedSensor = self.TrigBase.GetSensorObject(i)
            self.TrigBase.AddSensortoList(selectedSensor)
            index.Add(i)

        self.sampleRates = [[] for i in range(self.SensorsFound)]

        self.TrigBase.StreamData(index, newTransform, 2)
        
        
        self.threadManager()

    def Stop(self):
        """Callback to stop the data stream"""
        self.TrigBase.StopData()
        self.pauseFlag = True

    def Scan(self):
        """Callback to tell the base to scan for any available sensors"""
        f = self.TrigBase.ScanSensors().Result
        self.nameList = self.TrigBase.ListSensorNames()
        self.SensorsFound = len(self.nameList)

        self.TrigBase.ConnectSensors()
        return self.nameList
    
    def threadManager(self):
        """Handles the threads for the DataCollector gui"""
        self.emg_plot = deque()

        t1 = threading.Thread(target=self.streaming)

        t1.start()

def main():
    emg_obj = emg()
    emg_obj.Connect()
    emg_obj.Scan()
    emg_obj.Start()
    



if __name__ == "__main__":
    main()
