import utils

packages = utils.get_top_packages()
for p in packages:
    utils.download_wheel(p["project"], py_version="36", os_arch="manylinux1_x86_64")
