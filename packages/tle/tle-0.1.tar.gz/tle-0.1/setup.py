# pip works in your cwd. To install, you need setup.py. Basically, a
# path to here will be added to sys.path variable
# Note that tle.egg-info will be added (not sure what that is?).
#  - Install locally: pip install .
#  - Update: pip install . --upgrade

# To make updates easier, you can install w/ symlink so you don't have to 
# keep doing --upgrade
#   - Install with symlink: pip install -e .

# In this example, you can now import tle_proj from the python interpreter

# PUBLISH TO PyPI:
# - 1) run "python setup.py register" (follow steps, you may need to register)
# - 2) run "python setup.py sdist". This will create a "dist" directory w/ a tar.gz file.
# - 3) run "python setup.py sdist upload" to upload
from setuptools import setup

setup(name='tle',
      version='0.1',
      description='tle functions',
      author='John Doe',
      packages=['tle_proj'],
      zip_safe=False)