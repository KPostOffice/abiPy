import utils
import requests
import json
import auditwheel
import os

SESSION = requests.Session()

# py_version: python3.6 = 36, python2.7 = 27, python2 or python3 = py2.py3, python3 = py3
# os_arch = manylinux1_x86_64, manylinux1_i686, win32, win_amd64, macosx_10_6_intel...
def download_wheels(projects, release = "latest", py_version = None, os_arch = None):
    if not os.path.exists("wheels/"):
        os.mkdir("wheels")
    for p in projects:
        download_wheel(p, release, py_version, os_arch);

def download_wheel(project, release = "latest", py_version = None, os_arch = None):
    if not os.path.exists("wheels/"):
        os.mkdir("wheels")

    url = utils.get_json_url(project)
    response = SESSION.get(url)
    
    if response.status_code != 200:
        return

    data = response.json()
    
    if release == "latest":
        download_latest_wheel(data, py_version, os_arch)
        return

    if not data["releases"][release]:
        return

    for download in data["releases"][release]:
        info = download["filename"].split("-")
        if(download['packagetype'] == 'bdist_wheel' and
           (not py_version or utils.py_version_sat(py_version, download["python_version"])) and
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
           (not py_version or utils.py_version_sat(py_version, download["python_version"])) and
           (not os_arch or info[4] == "any.whl" or (os_arch + ".whl") == info[4])):
            url = download['url']
            local_filename = "wheels/" + url.split('/')[-1]
            if os.path.exists(local_filename):
                continue
            
            with requests.get(url, stream=True) as req:
                req.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in req.iter_content(chunk_size = 8192):
                        if chunk:
                            f.write(chunk)

    return

