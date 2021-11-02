
from time import sleep, time
from random import random
from tkinter.constants import X
import matplotlib.pyplot as plt

from block import block
from trial import trial
from motor import motor
from emg import emg


class framework():
    def __init__(self, COM, patID=1234, sess = 1, blocknum = 1):
        self.preload_max = .53
        self.preload_min = .51

        self.block = block(patID, sess=sess, blocknum=blocknum)

        self.mot = motor(COM, self.preload_max, self.preload_min)
        self.mot.start()
        # Give motor time to enable
        sleep(10)
        print("DONE Enabling motor")

        self.emg = emg()


    def fire(self,failure,trial_start_time):
        #TODO Add emg capture
        array = []
        self.emg.emg_trig_collection(array, 2000)
        print("FIRE! ",time()-trial_start_time,"  Failure:", failure)
        

        
        self.mot.fire()
        sleep(1)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.clear()
        
        # array = array[-500:]
        n = 3
        array = [avg for avg in [
            sum(array[i:i+n])/n for i in range(0, len(array), n)] for j in range(n)]
        xs = [i for i in range(0, 5001)]
        xs = xs[0:1*len(array)]
        
        print(len(xs), len(array))
        ax.plot(xs,array)

        # Format plot
        plt.title('EMG Readings')
        plt.ylim([0,.4])
        plt.ion()
        plt.show()
        
        sleep(1)
        self.mot.release()
        plt.pause(5)
        plt.close()
        self.current_trial.emg_data = array




    def preload_failure_handler(self, trial_start_time):
        """
        Checks for the patient to regain preloading. If they fail to do so by a certain time, they fail

        returns: Bool, true = Fire, false = Continue with other task
        """
        print("Preload failure")
        good_start_time = time()
        while(1):
            sleep(.01)
            if time()-good_start_time >= 1:
                print("Failure Recovery")
                return False

            if time()-trial_start_time >= 5:
                return True

             # Check if out of torque limits
            if self.mot.torque_preload_check() != 0:

                # Check if out of time for Failure Handler
                if time()-trial_start_time > 4:

                    self.current_trial.success = False

                    if self.mot.torque_preload_check() < 0:
                        self.current_trial.failure_reason = "prelow"
                    else:
                        self.current_trial.failure_reason = "prehigh"
                    return True
                else:
                    good_start_time = time()

    def preload_randomizer(self, trial_start_time):
        random_fire_time = time() + (5+trial_start_time-time()) * random()
        print("Random Fire Time:",random_fire_time-time())
        while(1):
            sleep(.1)
            # Check if preload amount is good
            if time()-random_fire_time > 0:
                return False

            # Check if out of torque limits
            if self.mot.torque_preload_check() != 0:
                # Check if out of time for Failure Handler
                if time()-trial_start_time > 4:

                    self.current_trial.success = False

                    if self.mot.torque_preload_check() < 0:
                        self.current_trial.failure_reason = "prelow"
                    else:
                        self.current_trial.failure_reason = "prehigh"

                # Call failure handler
                else:
                    if self.preload_failure_handler(trial_start_time):
                        return True
                    else:
                        return self.preload_randomizer(trial_start_time)

    def start_trial(self):
        if block:
            print("Starting Trial")
            self.current_trial = trial()
            trial_start_time = time()
            # Trial starts, debounce half a second
            sleep(.75)

            # Preload while checking torque for 2 seconds past start time
            failure = False
            while(1):
                sleep(.1)
                if time()-trial_start_time > 1.25:
                    break
                if  self.mot.torque_preload_check() != 0:
                    print(self.mot.torque_preload_check())
                    failure = self.preload_failure_handler(trial_start_time)
                    break
            
            # Randomizer
            if not failure:
                failure = self.preload_randomizer(trial_start_time)
            

            self.fire(failure, trial_start_time)

            while(time()-trial_start_time < 10):
                sleep(.1)
            


    def new_block():
        self.block = self.block.copy_block()

def main():
    try:
        frame = framework('COM15')
        sleep(1)
        for i in range(100):
            frame.start_trial()
        
    finally:
        frame.mot.exit()
        frame.emg.exit()
if __name__  == "__main__":
    main()
