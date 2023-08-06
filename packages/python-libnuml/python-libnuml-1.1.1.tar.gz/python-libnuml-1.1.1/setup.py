## @file    setup.py
## @brief   Python distutils code for libSEDML Python module (including dependencies)
## @author  Michael Hucka
## @author  Ben Bornstein
## @author  Ben Kovitz
## @author  Frank Bergmann (fbergman@caltech.edu)
## 
##<!---------------------------------------------------------------------------

import glob
import os
import sys
import shutil
import platform
from distutils.sysconfig import get_config_vars

current_dir = os.path.dirname(os.path.realpath(__file__))

# remove -Wstrict-prototypes
(opt,) = get_config_vars('OPT')
if opt != None:
  os.environ['OPT'] = " ".join(
      flag for flag in opt.split() if flag != '-Wstrict-prototypes'
  )

# we need to switch the __init__.py file based on the python version
# as python 3 uses a different syntax for metaclasses
if sys.version_info >= (3,0):
  # this is python 3.x
  if (os.path.exists(current_dir + '/libnuml/__init__.py')):
    os.remove(current_dir + '/libnuml/__init__.py')
  shutil.copyfile(current_dir + '/script/libnuml.py', current_dir + '/libnuml/__init__.py')
else:
  # this is an older python
  if (os.path.exists(current_dir + '/libnuml/__init__.py')):
    os.remove(current_dir + '/libnuml/__init__.py')
  shutil.copyfile(current_dir + '/script/libnuml.py', current_dir + '/libnuml/__init__.py')

# prepend the import statement that seems to be needed now 
with open(current_dir + '/libnuml/__init__.py', 'r') as original: data = original.read()
with open(current_dir + '/libnuml/__init__.py', 'w') as modified: modified.write("""

# import statement needed on some systems
import sys
import os.path
sys.path.append(os.path.dirname(__file__))

""" + data)
  
# figure out the os
#basepath = current_dir + '/base/'
basepath = './base/'
current_os = 'LINUX'
package_name = '"libnuml"'
inc_dirs = ['swig']
lib_dirs = []
libs = []
definitions = []
packages = [
  ('LIBSBML_USE_LEGACY_MATH', None)
]
if platform.system() == 'Darwin': 
  current_os = 'DARWIN'
elif platform.system() == 'Windows':
  current_os = 'WIN32'
  package_name = '\\"libsbml\\"'
  definitions = [
    ('LIBSEDML_EXPORTS', None),
    ('LIBNUML_STATIC', None),
    ('LIBSBML_STATIC', None),
    ('LIBSEDML_STATIC', None),
    ('LIBLAX_STATIC', None)
  ]

definitions = definitions  + [
  ('HAVE_MEMMOVE', None),
  ('_LIB', None)
  ]
  
  
cfiles = [ basepath + 'libnuml_wrap.cpp' ]

# add dependencies
cfiles = cfiles + glob.glob(basepath + "*.c");

for root, dirs, files in os.walk(basepath + 'sbml'):
  for file in files:
    if file.endswith('.c') or file.endswith('.cpp'):
      cfiles.append(os.path.join(root, file))

for root, dirs, files in os.walk(basepath + 'numl'):
  for file in files:
    if file.endswith('.c') or file.endswith('.cpp'):
      cfiles.append(os.path.join(root, file))
for root, dirs, files in os.walk(basepath + 'sedml'):
  for file in files:
    if file.endswith('.c') or file.endswith('.cpp'):
      cfiles.append(os.path.join(root, file))


from distutils.core import setup, Extension
try:
    import distutils.command.bdist_conda
except:
    pass

setup(name             = "python-libnuml",
      version          = "1.1.1",
      description      = "LibNuML Python API",
      long_description = ("libNuML is a library for reading, writing and "+
                          "manipulating NuML.  It is written in ISO C and C++, supports "+
                          "NuML Levels 1, Version 1, and runs on Linux, Microsoft "+
                          "Windows, and Apple MacOS X.  For more information "+
                          "about SEDML, please see http://github.com/numl/numl/."),
      license          = "BSD",
      author           = "Frank T. Bergmann",
      author_email     = "fbergman@caltech.edu",
      url              = "https://github.com/NuML/NuML/tree/master/libnuml",
      packages         = ["libnuml"],
      package_dir      = {'libnuml': 'libnuml'},
      #data_files       = [('lib/site-packages', ['llibnuml.pth'])],
      ext_package      = "libnuml",
      ext_modules      = [Extension("_libnuml", 
                            sources = cfiles,
                            define_macros =  definitions +
                            [ (current_os, None), 
                              ('USE_EXPAT', None) 
                            ] 
                            + packages,
                            include_dirs = inc_dirs +
                            [ 
                              basepath + "/",
                              basepath + "/swig",
                              basepath + "/sbml", 
                              basepath + "/sbml/compress", 
                              basepath + "/sbml/validator/constraints", 
                              basepath + "/sbml/packages/comp/validator", 
                              basepath + "/sbml/packages/comp/validator/constraints", 
                              "."],
                            libraries = libs,
                            library_dirs = lib_dirs
                            )
                         ]
)
