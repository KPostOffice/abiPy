import requests
import json
import auditwheel

TOP_PACKAGES_FILE = "top-pypi.json"
BASE_URL = "https://pypi.org/pypi/"
SESSION = requests.Session()

# TODO: check if file already exists

def get_json_url(package_name):
    return BASE_URL + package_name + "/json"

# TODO: make wheel directory if it doesn't exist
# py_version: python3.6 = 36, python2.7 = 27, python2 or python3 = py2.py3, python3 = py3
# os_arch = manylinux1_x86_64, manylinux1_i686, win32, win_amd64, macosx_10_6_intel...
def download_wheels(projects, release = "latest", py_version = None, os_arch = None):
    for p in projects:
        download_wheel(p, release, py_version, os_arch);

def download_wheel(project, release = "latest", py_version = None, os_arch = None):
    url = get_json_url(project)
    response = SESSION.get(url)
    response.raise_for_status();
    data = response.json()
    
    if release == "latest":
        download_latest_wheel(data, py_version, os_arch)
        return

    if not data["releases"][release]:
        return

    for download in data["releases"][release]:
        info = download["filename"].split("-")
        if(download['packagetype'] == 'bdist_wheel' and
           (not py_version or py_version_sat(py_version, download["python_version"])) and
           (not os_arch or info[4] == "any.whl" or (os_arch + ".whl") == info[4])):
            url = download['url']
            local_filename = "wheels/" + url.split('/')[-1]
            with requests.get(url, stream=True) as req:
                req.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in req.iter_content(chunk_size = 8192):
                        if chunk:
                            f.write(chunk)

    return

def download_latest_wheel(data, py_version = None, os_arch = None):
    for download in data['urls']:
        info = download["filename"].split("-")            
        if(download['packagetype'] == 'bdist_wheel' and
           (not py_version or py_version_sat(py_version, download["python_version"])) and
           (not os_arch or (os_arch + ".whl") == info[4])):
            url = download['url']
            local_filename = "wheels/" + url.split('/')[-1]
            with requests.get(url, stream=True) as req:
                req.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in req.iter_content(chunk_size = 8192):
                        if chunk:
                            f.write(chunk)

    return

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

