from block import block
import json


def JSONmaker(blockobject):
    jdict = {"block":
             {"info":
              {"patID": blockobject.patID,
               "date": blockobject.dte,
               "session": blockobject.session,
               "blocknum": blockobject.blocknum},
              "results":
                  {"avgsuccess": blockobject.compute_avg_success(),
                   "numoftrials": blockobject.number_of_trials()},
                  "trials":
                  {}}}

    i = 0
    for t in blockobject.trials:
        i += 1
        jdict["block"]["trials"].update({f"trial{i}":
                                         {"success": t.success,
                                          "failure-reason": t.failure_reason,
                                          "peakvalue": t.peak,
                                          "emgdata": t.emg_data}})

    jfile = json.dump(jdict)


def main():
    blockobject = block()
    print(blockobject.date)
    CreateJSON.JSONmaker(blockobject)


if __name__ == "__main__":
    main()
