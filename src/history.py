#!/bin/python3
"""
# Description:
History management

# Authors:
- Seth Giovanetti
- Oscar Contreras
"""

import os
from Codes import Code

os.makedirs("history", exist_ok=True)

SEP = chr(7)
# MESSAGE_SEP = chr(31)
# fileTerminator = chr(31) + Code.HISTORY_RESP.value + chr(0) # Message Separator + Code + NullByte


def getFile(session_id):
    return os.path.join("history", "{}.txt".format(session_id))
    #directory = os.path.join("history", "{}".format(session_id))
    #exists = os.path.isdir(directory)
    #print(session_id, " directory? ", exists)

    #if not os.path.exists(directory):
    #    os.makedirs(directory)

    #return os.path.join(directory, "{}.txt".format(session_id))


def append(session_id, sender, message):
    with open(getFile(session_id), "a", newline="\n") as histfile:
        # histfile.write(sender + SEP + message + "\n" + fileTerminator)
        histfile.write(sender + SEP + message + "\n")

def endInstance(session_id):
    with open(getFile(session_id), "a", newline="\n") as histfile:
        #print("End Session Instance")
        histfile.write("EndSession\n")

def get(session_id):
    ses = 1
    sessNum = str(ses)
    pathToFile = getFile(session_id)
    exists = os.path.isfile(pathToFile)
    if exists:
        with open(pathToFile, "r", newline="\n") as histfile:
            for line in histfile:
                if line == "EndSession\n":
                    ses = ses + 1
                    sessNum = str(ses)
                    yield (str(0), "", "")
                else:
                    (cid, msg) = line.split(SEP)
                    yield (sessNum, cid, msg)

                #(cid, msg) = line.split(SEP)
                #yield (cid, msg)    
                # print("hist line "+ repr(line))
                # if(line == fileTerminator):
                #     print("fileTerminator hist line")
                # else:
                #     (cid, msg) = line.split(SEP)
                #     yield (cid, msg)
    else:
        yield (str(-1), "No history found for that user.", "")
