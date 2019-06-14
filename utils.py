import json
import re

TOP_PACKAGES_FILE = "top-pypi.json"
BASE_URL = "https://pypi.org/pypi/"

def get_json_url(package_name):
    return BASE_URL + package_name + "/json"


def py_version_sat(py_version, pip_py_version):
    if pip_py_version[0:2] == "cp":
        if re.match( re.escape(pip_py_version) + r'.*', ("cp" + py_version)):
            return True
        return False

    if pip_py_version[0:2] == "ip":
        if re.match( re.escape(pip_py_version) + r'.*', ("ip" + py_version)):
            return True
        return False
    
    if pip_py_version[0:2] == "pp":
        if re.match( re.escape(pip_py_version) + r'.*', ("pp" + py_version)):
            return True
        return False

    if pip_py_version[0:2] == "jy":
        if re.match( re.escape(pip_py_version) + r'.*', ("jy" + py_version)):
            return True
        return False
    
    pyx = pip_py_version.split(".")
    for ver in pyx:
        if re.match(ver + r'.*', ("py" + py_version[0])):
            return True
        elif re.match( ver + r'.*', ("cp" + py_version)):
            return True
        elif re.match( ver + r'.*', ("ip" + py_version)):
            return True
        elif re.match( ver + r'.*', ("pp" + py_version)):
            return True
        elif re.match( ver + r'.*', ("jy" + py_version)):
            return True

    return False
    

    

def get_top_packages():
    with open(TOP_PACKAGES_FILE) as f:
        data = json.load(f)

    return data["rows"]

