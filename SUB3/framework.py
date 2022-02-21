
import threading
from time import sleep, time
from random import random

from block import block
from trial import trial
from motor import motor
from emg import emg
from create_json import JSONmaker
import scipy as sp
from scipy import signal
import peak


class framework():
    def __init__(self, COM, patID=1234, sess=1, blocknum=1, premin=.51, premax=.53, no_motor = False, no_emg = False):
        self.preload_max = premax
        self.preload_min = premin

        self.block = block(patID, sess=sess, blocknum=blocknum)

        if not no_motor:
            self.mot = motor(COM, self.preload_max, self.preload_min)
            self.mot.start()
            # Give motor time to enable
            sleep(10)
            print("Done Enabling motor")
        else:
            self.mot = None
        if not no_emg:
            self.emg = emg()
        else:
            self.emg = None
        
        # This bit stops the block
        self.running = False

        # This bit pauses the block
        self.paused = False

        # This bit generates emg signal
        self.show_emg = False

        self.starting_trial = False
        

    def exit(self):
        self.running = False
        if self.mot:
            self.mot.exit()
        else:
            print("No Motor, Exiting")
        if self.emg:
            self.emg.exit()
        else:
            print("No EMG, Exiting")

    def fire(self, failure, trial_start_time):
        # TODO Add emg capture
        
        print("FIRE! ", time()-trial_start_time, "  Failure:", failure)
        self.mot.fire()
        sleep(2)

        self.mot.release()

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
        print("Random Fire Time:", random_fire_time-time())
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

    def take_trial(self):
        if self.paused:
           sleep(1) 
        else:
            self.starting_trial = True
            if not self.mot or not self.emg:
                print("Missing EMG or Motor, Skipping Trial")
                self.current_trial = trial()
                sleep(4)
                return

            if self.block:
                print("Starting Trial")
                self.current_trial = trial()
                trial_start_time = time()
                trial_data = [[],[]]
            
                self.emg.start_cont_collect(trial_data)
                # Trial starts, debounce half a second
                sleep(.75)

                # Preload while checking torque for 2 seconds past start time
                failure = False
                while(1):
                    sleep(.1)
                    if time()-trial_start_time > 1.25:
                        break
                    if self.mot.torque_preload_check() != 0:
                        failure = self.preload_failure_handler(trial_start_time)
                        break

                # Randomizer
                if not failure:
                    failure = self.preload_randomizer(trial_start_time)

                if not self.paused:
                    self.fire(failure, trial_start_time)
                else:
                    self.emg.stop_cont_collect()
                    return

                self.emg.stop_cont_collect()

                # Filter and save the data to the trial
                sfreq = 1925
                low_pass = 5
                low_pass = low_pass/(sfreq/2)
                b2, a2 = sp.signal.butter(4, low_pass, btype='lowpass')
                self.current_trial.emg_data = sp.signal.filtfilt(
                    b2, a2, trial_data[0]).tolist()
                self.current_trial.acc_data = trial_data[1]

                # self.current_trial.peak = peak.simple_peak(self.current_trial)
                # self.current_trial.peak = peak.wave_avg(self.current_trial)

                # Display the EMG
                self.show_emg = True

                self.block.trials.append(self.current_trial)
                while(time()-trial_start_time < 10):
                    sleep(.1)

    # Update preload values
    def update_preloads(self,pre_min, pre_max):
        self.premin = pre_min
        self.premax = pre_max

    def new_block(self):
        self.block = self.block.copy_block()

    def pause(self):
        if self.paused:
            self.paused= False
        else:
            self.paused= True
        

    def stop(self):
        self.running = False
        self.paused = True
        b = self.block
        with open(f'PID{b.patID}/{b.date[2:].replace("-", "")}-Block{b.blocknum}.json', "w") as file:
            JSONmaker(self.block, file)
        self.new_block()
        

    def start(self):
        self.running = True
        self.paused = False
        self.trial_thread = threading.Thread(
            target=self._data_collection_thread)
        self.trial_thread.start()

    def _data_collection_thread(self):
        while(self.running):
            self.take_trial()
