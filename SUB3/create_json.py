from block import block
from trial import trial
import json


def JSONmaker(blockobject: block, file):
    jdict = {"block":
             {"info":
              {"patID": blockobject.patID,
               "date": blockobject.date,
               "session": blockobject.session,
               "blocknum": blockobject.blocknum},
              "results":
                  {"avgsuccess": blockobject.compute_avg_success(),
                   "numoftrials": blockobject.number_of_trials()},
                  "trials":
                  {}}}

    i = 0
    for t in blockobject.trials:
        t: trial
        i += 1
        jdict["block"]["trials"].update({f"trial{i}":
                                            {"success": t.success,
                                            "failure-reason": t.failure_reason,
                                            "peakvalue": t.peak,
                                             "maxdelayms": t.max_delay_ms,
                                            "emgdata": t.emg_data,
                                            "accdata": t.acc_data
                                            }
                                        })

    json.dump(jdict, file, indent=4)


def main():
    blockobject = block()
    print(blockobject.date)
    JSONmaker(blockobject)


if __name__ == "__main__":
    main()
