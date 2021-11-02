

class trial():
    def __init__(self):
        self.emg_data = []
        self.success = False
        self.peak = 0
        self.failure_reason = "none" 
        """
            Potential failure reasons
            "prelow" - Patient failed by not maintaining preload on low end
            "prehigh" - Patient failed by not maintaining preload on high end
            "mwave" - Patient failed by having too large a peak mwave
        """
