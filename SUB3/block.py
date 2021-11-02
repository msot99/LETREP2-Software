from datetime import date


class block():
    def __init__(self, patID = 1234, dte = str(date.today()), sess = 1, blocknum = 1 ):
        self.patID = patID 
        self.date = dte
        self.session = sess
        self.blocknum = blocknum
        self.trials = list()

    def compute_avg_success(self) -> None:
        #TODO compute average success rate based off of data in trails
        pass
    
    def number_of_trials(self):
        return len(self.trials)
    
    def copy_block(self):
        return block(self.patID, self.date, self.session, self.blocknum + 1)
        