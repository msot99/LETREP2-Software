
from time import sleep, time
from random import random
from tkinter.constants import X

from block import block
from trial import trial
from motor import motor
from emg import emg


class framework():
    def __init__(self):
        self.preload_max = 5.3
        self.preload_min = 5.1
        self.mot = None

    def preload_failure_handler(self, trial_start_time):
        """
        Checks for the patient to regain preloading. If they fail to do so by a certain time, they fail

        returns: Bool, true = Fire, false = Continue with other task
        """
        good_start_time = time()
        while(1):
            if time()-good_start_time >= 1:
                return False

            if time()-trial_start_time >= 5:
                return True

             # Check if out of torque limits
            if self.mot.torque_preload_good() != 0:

                # Check if out of time for Failure Handler
                if time()-trial_start_time > 4:

                    self.current_trial.success = False

                    if self.mot.torque_preload_good() < 0:
                        self.current_trial.failure-reason = "prelow"
                    else:
                        self.current_trial.failure-reason = "prehigh"
                    return True
                else:
                    good_start_time = time()

    def preload_randomizer(self, trial_start_time):
        random_fire_time = trial_start_time + (5-trial_start_time) * random()

        while(1):
            # Check if preload amount is good
            if time()-random_fire_time > 0:
                return False

            # Check if out of torque limits
            if self.mot.torque_preload_good() != 0:

                # Check if out of time for Failure Handler
                if time()-trial_start_time > 4:

                    self.current_trial.success = False

                    if self.mot.torque_preload_good() < 0:
                        self.current_trial.failure-reason = "prelow"
                    else:
                        self.current_trial.failure-reason = "prehigh"

                # Call failure handler
                else:
                    if self.preload_failue_handler(trial_start_time):
                        return True
                    else:
                        return self.preload_randomizer(trial_start_time)

    def start_trial(self):
        if block:

            self.current_trial = trial()
            trial_start_time = time()
            # Trial starts, debounce half a second
            sleep(.5)

            # Preload while checking torque for 2 seconds past start time
            failure = False
            while(1):
                if time()-trial_start_time > 2:
                    break
                if (mot.torque > self.preload_max) and (mot.torque < self.preload_min):
                    failure = self.preload_failue_handler(trial_start_time)
                    break

            # Randomizer
            if not failure:
                failure = self.preload_randomizer(trial_start_time)

            # TODO Add self.fire(failure)

    def new_block():
        pass
