from threading import Thread
from time import sleep


class TheClass:

    def __init__(self, com, max, min):
        self.com = com
        self.max = max
        self.min = min

    def fun(self):
        sleep(1)
        print("A")
    
    def createThread(self):
        thread = Thread(target=self.fun)
        print("C")
        sleep(2)
        print("B")
        thread.start()

if __name__ == "__main__":
    mot = TheClass("COM15", .51,.53)
    mot.createThread()