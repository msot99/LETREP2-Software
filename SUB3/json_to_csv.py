import csv
import json

def json_to_csv(json_file, csv_file):
    jdict = json.load(json_file)

    trials = jdict["block"]["trials"]
    trials = list(trials.values())

    for i, trial in enumerate(trials):
        csv_file.write(f"Trial {i} emg,")
        for acc in trial["emgdata"]:
            csv_file.write(str(acc) + ",")
        csv_file.write(f"\nTrial {i} acc,")
        for acc in trial["accdata"]:
            csv_file.write(str(acc) + ",")
        csv_file.write("\n")

def main():
    with open("myfile.json", "r") as json_file:
        with open("myfile.csv", "w") as csv_file:
            json_to_csv(json_file, csv_file)

if __name__ == "__main__":
    main()