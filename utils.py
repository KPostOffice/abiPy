import json

TOP_PACKAGES_FILE = "top-pypi.json"
BASE_URL = "https://pypi.org/pypi/"

def get_json_url(package_name):
    return BASE_URL + package_name + "/json"


def py_version_sat(py_version, pip_py_version):
    if pip_py_version[0:2] == "cp":
        if ("cp" + py_version) == pip_py_version:
            return True
        return False

    pyx = pip_py_version.split(".")
    if ("py" + py_version[0]) in pyx:
        return True

    return False
    

    

def get_top_packages():
    with open(TOP_PACKAGES_FILE) as f:
        data = json.load(f)

    return data["rows"]

