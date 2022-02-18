from os import listdir
from os.path import isfile, join, splitext
import json
from block import block

# Opens all json files in a directory and returns 2D list
# [[Block1,Block2,Block3],
#  [Block1,Block2,Block3]]
#
def open_json_files(directory):

    sessions = {}

    # Get only json files
    json_files = [join(directory,f) for f in listdir(directory) if isfile(
        join(directory, f)) and splitext(join(directory, f))[1] == ".json"]
    
    # Open all JSON files
    for f in json_files:
        
        with open(f, "r") as json_file:
            jdict = json.load(json_file)
            blk = block(jdict["block"])
            if blk.session in sessions.keys():
                sessions[blk.session].append(blk)
            else:
                sessions[blk.session] = [blk]


    return sessions


