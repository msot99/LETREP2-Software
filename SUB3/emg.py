import clr
clr.AddReference(
    "C:/Users/jesse/Desktop/LETREP2-Software/SUB3/resources/DelsysAPI")
clr.AddReference("System.Collections")
from System import Int32
from System.Collections.Generic import List
from Aero import AeroPy
from collections import deque
import threading
from DataManager import DataKernel

from time import sleep

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
        self.temp_emg_storage = []

        self._emg_collect = False
        self._cont_emg = False
        self.emg_data_collected = False
        self._start_collect = False

        base = TrignoBase()
        self.TrigBase = base.BaseInstance
        self.TrigBase.ValidateBase(key, license, "RF")

        #scan for any available sensors
        self.TrigBase.ScanSensors().Result
        self.SensorsFound = len(self.TrigBase.ListSensorNames())
        self.TrigBase.ConnectSensors()

       # start the data stream from Sensors
        newTransform = self.TrigBase.CreateTransform("raw")
        self.index = List[Int32]()

        self.TrigBase.ClearSensorList()

        for i in range(self.SensorsFound):
            selectedSensor = self.TrigBase.GetSensorObject(i)
            self.TrigBase.AddSensortoList(selectedSensor)
            self.index.Add(i)

        self.TrigBase.StreamData(self.index, newTransform, 2)

        self.threadManager()
    def emg_trig_collect(self):
        self._emg_collect = True

    def start_cont_collect(self):
        self._cont_emg = True

    def _read_emg(self,temp_array):
        dataReady = self.TrigBase.CheckDataQueue()
        if dataReady:
            DataOut = self.TrigBase.PollData()
            # print(list(DataOut))
            temp_array.extend([abs(sample)
                                    for sample in list(DataOut)[0][0]])

    def streaming(self):
        """This is the data processing thread"""
        while(self._emg_collect):

            if self._cont_emg:
                self._read_emg(self.array_to_store)
                self.emg_data_collected = True
            
            elif self._emg_collect:

                while(len(self.array_to_store)<2000):
                    sleep(.01)
                    self._read_emg(self.array_to_store)

                self._emg_collect = False
            else:
                dead_array = []
                self._read_emg(dead_array)

    def stop(self):
        """Callback to stop the data stream"""
        self.TrigBase.StopData()
        self._emg_collect = False
        if hasattr(self, "t1"):
            self.t1.join()

    def threadManager(self):
        """Handles the threads for the DataCollector gui"""
        self._emg_collect = True

        self.t1 = threading.Thread(target=self.streaming)

        self.t1.start()

def main():
    arr = []
    emg_obj = emg(arr)
    input()
    print("TrigCollect")
    # emg_obj.start_cont_collect()
    emg_obj.emg_trig_collect()
    input()
    emg_obj.stop()
    print(arr)

if __name__ == "__main__":
    main()