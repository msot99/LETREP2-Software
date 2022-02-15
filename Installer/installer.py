
import os

import getpass
username = getpass.getuser()


import distutils.dir_util
from email.mime import base
import shutil

base_install = "C:/Program Files/LETREP2"
from_dir = "./resources"
to_dir = base_install+"/resources"
distutils.dir_util.copy_tree(from_dir, to_dir)


shutil.copy('LETREP2 Software.exe', "C:/Users/%s/Desktop"% username)

