from auditwheel import wheel_abi
import os
import pprint
import json

DIRECTORY = "wheels/"

def extract():
    list_ = []
    for filename in os.listdir(DIRECTORY):
        try:
            a = wheel_abi.analyze_wheel_abi(DIRECTORY + filename)
        except:
            print(f"{filename} ")
            continue

        project  = filename.split("-")[0]
        curr_obj = {"project": project, "data": {"analyze_wheel_abi": {}}}

        for so in a.versioned_symbols:
            curr_obj["data"]["analyze_wheel_abi"][so] = []
            for sym in a.versioned_symbols[so]:
                curr_obj["data"]["analyze_wheel_abi"][so].append(sym)
            
        list_.append(curr_obj)

    return list_
