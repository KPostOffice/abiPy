import json


class AbiVecs():
    def __init__(self, abi_data: list):
        self.sizes = []
        self.positions = []
        self.build_data = {}
        self.gen_build_data(abi_data)
        self.vectors = self.abi2vec_many(abi_data)

    def all_build_data(self):
        return {'sizes': self.sizes, 'positions': self.positions, 'build_data': self.build_data}
    
    def insert_so_if_not_exist(self, so: str):
        if so in self.build_data:
            return

        self.build_data[so] = {
            "pos": len(self.positions),
            "symbols": {}
        }

        self.sizes.append(0)
        
        if len(self.positions) == 0:
            self.positions.append(1)
        else:
            self.positions.append(self.positions[-1] + self.sizes[-2])

    def insert_sym_if_not_exist(sym: str, so: str):

        if sym in self.build_data[so]["symbols"]:
            return

        pos = self.build_data[so]["pos"]
        self.build_data[so]["symbols"][sym] = self.sizes[pos]
        self.sizes[pos] = self.sizes[pos] + 1
        self.positions[pos+1:] = [v + 1 for v in self.positions[pos+1:]]

    def gen_build_data(abi_data: list):
        for whl in abi_data:
            for so in whl["data"]["analyze_wheel_abi"]:
                self.insert_so_if_not_exist(so)
                for sym in whl["data"]["analyze_wheel_abi"][so]:
                    self.insert_sym_if_not_exist(sym, so)

        return

    def abi2vec_single(whl: dict, size: int) -> list:

        if whl["data"]["analyze_wheel_abi"] == {}:
            return [0] * size
    
        to_ret = [1] * size
        for so in whl["data"]["analyze_wheel_abi"]:
            pos = self.build_data[so]["pos"]
            start = self.positions[pos]
            lib_size = self.sizes[pos]
            to_ret[start:start+lib_size] = [0] * lib_size
        
            for sym in whl["data"]["analyze_wheel_abi"][so]:
                to_ret[start + self.build_data[so]["symbols"][sym]] = 1

        return to_ret

    def abi2vec_many(abi_data: list):
        size = self.positions[-1] + self.sizes[-1]
        to_ret = {}
        for whl in abi_data:
            to_ret[whl["project"]] = self.abi2vec_single(whl, size)

        return to_ret

with open("abi_data.json", "r") as f:
    dat = json.loads(f.read())

gen_build_data(dat)
with open("build_data.json", "w+") as f:
    f.write(json.dumps({"positions": self.positions, "sizes": self.sizes, "build_data": self.build_data}))

with open("vecs.json", "w+") as f:
    f.write(json.dumps(abi2vec_many(dat)))
