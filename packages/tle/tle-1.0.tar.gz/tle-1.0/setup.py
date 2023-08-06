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
# - 1) Get twine (more secure) by running "pip install twine"
# - 2) Register at https://pypi.python.org/pypi
# - 2) run "python setup.py sdist". This will create a "dist" directory w/ a tar.gz file.
# - 3) run "twine upload dist/*" and follow instructions
#  Now you can do "pip install tle"

# Also check out python setup.py --help-commands
from setuptools import setup

setup(name='tle', # Use this to do the 'pip install tle'
      version='1.0',
      description='tle functions',
      author='John Doe',
      packages=['tle_proj'], # The name of the package that will be imported 'import tle_proj'
      zip_safe=False)