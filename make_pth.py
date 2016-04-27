import os
import shutil
from distutils.sysconfig import get_python_lib
print get_python_lib()
def cur_file_dir():
    return os.path.split(os.path.realpath(__file__))[0]
pth_name = 'qar_dep.pth'
local_path = os.path.join(cur_file_dir(), pth_name)
f = open(local_path, 'w')
f.write(cur_file_dir())
f.close()
shutil.copy(local_path, os.path.join(get_python_lib(), pth_name))