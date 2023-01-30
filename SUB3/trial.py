class trial():
    def __init__(self):
        self.emg_data = []
        self.success = True
        self.peak = 0
        self.speed = 175
        self.max_delay_ms = 0
        self.failure_reason = "none"
        self.acc_data = []
        self.max_delay_ms = 0
        """
            Potential failure reasons
            "prelow" - Patient failed by not maintaining preload on low end
            "prehigh" - Patient failed by not maintaining preload on high end
            "mwave" - Patient failed by having too large a peak mwave
        """

    def obj_from_json(self, json):
        self.emg_data = json['emgdata']
        self.success = json['success']
        self.peak = json['peakvalue']
        self.speed = json['speed']
        self.failure_reason = json['failure-reason']
        self.acc_data = json['accdata']
        self.max_delay_ms = json['maxdelayms']

        return self