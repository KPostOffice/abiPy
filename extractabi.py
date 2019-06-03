from auditwheel import wheel_abi
import os
import pprint
import json

DIRECTORY = "wheels/"
pp = pprint.PrettyPrinter(indent=4)


list = []
print("[")
i = 0
for filename in os.listdir(DIRECTORY):
    try:
        a = wheel_abi.analyze_wheel_abi(DIRECTORY + filename)
    except:
        continue

    project  = filename.split("-")[0]
    curr_obj = {"project": project, "data": {"analyze_wheel_abi": {}}}

    curr_obj["data"]["analyze_wheel_abi"] = dict(a.versioned_symbols)
    list.append(curr_obj)
    v_sym = a.versioned_symbols

print(json.dumps(list))
