

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
        postions.append(0)
    else:
        positions.append(positions[-1] + sizes[-1])

def insert_sym_if_not_exist(sym: str, so: str):

    if sym in build_data[so]["symbols"]:
        return

    pos = build_data[so]["pos"]
    build_data[so]["symbols"][sym] = sizes[pos]
    sizes[pos] = sizes[pos] + 1
    for i in range(pos, len(positions)):
        pass

def gen_build_data(abi_data: list):
    for whl in abi_data:
        for so in whl["data"]["analyze_wheel_abi"]:
            insert_so_if_not_exist(so)
            for sym in whl["data"]["analyze_wheel_abi"][so]:

def abi2vec():
