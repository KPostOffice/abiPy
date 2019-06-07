import json

sizes = []
positions = []
build_data = {}

def insert_so_if_not_exist(so: str):
    if so in build_data:
        return

    build_data[so] = {
        "pos": len(positions),
        "symbols": {}
    }

    sizes.append(0)
    
    if len(positions) == 0:
        positions.append(1)
    else:
        positions.append(positions[-1] + sizes[-2])

def insert_sym_if_not_exist(sym: str, so: str):

    if sym in build_data[so]["symbols"]:
        return

    pos = build_data[so]["pos"]
    build_data[so]["symbols"][sym] = sizes[pos]
    sizes[pos] = sizes[pos] + 1
    positions[pos+1:] = [v + 1 for v in positions[pos+1:]]

def gen_build_data(abi_data: list):
    for whl in abi_data:
        for so in whl["data"]["analyze_wheel_abi"]:
            insert_so_if_not_exist(so)
            for sym in whl["data"]["analyze_wheel_abi"][so]:
                insert_sym_if_not_exist(sym, so)

    return

def abi2vec_single(whl: dict, size: int) -> list:

    if whl["data"]["analyze_wheel_abi"] == {}:
        return [0] * size
    
    to_ret = [1] * size
    for so in whl["data"]["analyze_wheel_abi"]:
        pos = build_data[so]["pos"]
        start = positions[pos]
        lib_size = sizes[pos]
        to_ret[start:start+lib_size] = [0] * lib_size
        
        for sym in whl["data"]["analyze_wheel_abi"][so]:
            to_ret[start + build_data[so]["symbols"][sym]] = 1

    return to_ret

def abi2vec_many(abi_data: list):
    size = positions[-1] + sizes[-1]
    to_ret = {}
    for whl in abi_data:
        to_ret[whl["project"]] = abi2vec_single(whl, size)

    return to_ret

with open("abi_data.json", "r") as f:
    dat = json.loads(f.read())

gen_build_data(dat)
with open("build_data.json", "w+") as f:
    f.write(json.dumps({"positions": positions, "sizes": sizes, "build_data": build_data}))

with open("vecs.json", "w+") as f:
    f.write(json.dumps(abi2vec_many(dat)))
