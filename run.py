import load_whls
import extractabi
import json
import os
import shutil
from abi2vec import AbiVecs

DATA_FILE = "abi_data.json"

class WheelData():
    def __init__(self, projects: list, py_versions: list, os_archs: list, release='latest'):
        self.projects = projects
        self.py_versions = py_versions
        self.os_archs = os_archs
        self.release = release
        self.abi_data = []
        self.abivecs = None

    def download(self, force=False):
        if force and os.path.exists('wheels/'):
            shutil.rmtree('wheels/')
            
        for p in self.py_versions:
            for oa in self.os_archs:
                print(f'PyVers: {p}; OSARCH: {oa}')
                load_whls.download_wheels(self.projects, self.release, p, oa)

    def extract_abi_data(self):
        self.abi_data = extractabi.extract()

    def abi_data_from_file(self, filename: str):
        with open(filename, 'r') as f:
            self.abi_data = json.loads(f.read())
            
    def construct_vecs(self):
        self.abivecs = AbiVecs(self.abi_data)

    def dump2file(self):
        with open('abi_data.json', 'w+') as f:
            f.write(json.dumps(self.abi_data))

        with open('vecs.json', 'w+') as f:
            f.write(json.dumps(self.abivecs.vectors))

        with open('build_data.json', 'w+') as f:
            f.write(json.dumps(self.abivecs.all_build_data()))
