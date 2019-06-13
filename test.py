from run import WheelData
import utils
######################
#  DO THE DOWNLOAD   #
######################
packages_plus = utils.get_top_packages()[:200]
projects = []
for p in packages_plus:
    projects.append(p['project'])

whld = WheelData(projects, ['36'], ['manylinux1_x86_64', 'linux_x86_64', 'manylinux2010_x86_64', 'any'])
whld.download(force = True)
whld.extract_abi_data()
whld.construct_vecs()
whld.dump2file()
