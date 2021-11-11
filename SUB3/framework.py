
import threading
from time import sleep, time
from random import random

from block import block
from trial import trial
from motor import motor
from emg_copy import emg


class framework():
    def __init__(self, COM, patID=1234, sess=1, blocknum=1, premin=.51, premax=.53):
        self.preload_max = premax
        self.preload_min = premin

        self.block = block(patID, sess=sess, blocknum=blocknum)

        self.mot = motor(COM, self.preload_max, self.preload_min)
        self.mot.start()
        # Give motor time to enable
        sleep(10)
        print("DONE Enabling motor")
        self.emg = emg()
        self.running = False
        self.show_emg = False

    def exit(self):
        self.mot.exit()
        self.emg.exit()

    def fire(self, failure, trial_start_time):
        # TODO Add emg capture
        array = []
        print("FIRE! ", time()-trial_start_time, "  Failure:", failure)
        self.current_trial.emg_data = array
        self.emg.emg_trig_collection(array, 600)
        self.mot.fire()
        sleep(2)
        self.show_emg = True
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
        if self.block:
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
                if self.mot.torque_preload_check() != 0:
                    # print(self.mot.torque_preload_check())
                    failure = self.preload_failure_handler(trial_start_time)
                    break

            # Randomizer
            if not failure:
                failure = self.preload_randomizer(trial_start_time)

            if self.running:
                self.fire(failure, trial_start_time)
            else:
                return

            self.block.trials.append(self.current_trial)
            while(time()-trial_start_time < 10):
                sleep(.1)

    def new_block(self):
        self.block = self.block.copy_block()

    def stop(self):
        self.running = False

    def start(self):
        self.running = True
        self.trial_thread = threading.Thread(
            target=self._data_collection_thread)
        self.trial_thread.start()

    def _data_collection_thread(self):
        while(self.running):
            self.take_trial()


def main():
    try:
        frame = framework('COM15')
        sleep(1)
        for i in range(100):
            frame.start_trial()

    finally:
        frame.mot.exit()
        frame.emg.exit()


if __name__ == "__main__":
    main()
