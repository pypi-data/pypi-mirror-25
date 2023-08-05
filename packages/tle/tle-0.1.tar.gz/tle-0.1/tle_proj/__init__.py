# __name__ and __package__ will be global objects on every module and the running script.

# On startup, python will add the directory the script is located in to sys.path, NOT the CWD

# When evaluating imports, python will FIRST look to the base directory added so sys.path.
# IF NOT FOUND THERE, THEN it will look in subdirectories with __init__.py.

# Search order:
# - built in module
# - File name in one of the sys.path directories 
#   - Directory of the main script is added here
# - PYTHONPATH env

# If searching for package, python will look for subdirectories of sys.path that have
# an __init__.py file. Then, it will continue searching subdirectories from there w/
# __init__.py
# EXAMPLE of importing module in a package subdir: 
#  - import sub_dir_of_sys_path_with_init_file.my_module

# The __name__ of a module is based on how it was LOADED, NOT where it is LOCATED. If
# found in the directory located in sys.path, it will NOT have the 'full' name.
# EXAMPLE running from root.py
# - executing root.py, if you import sub_dir.my_module, the __name__ of my_module will be "sub_dir.my_module"
# - executing sub_dir_2.py, if you import my_module, the __name__ of my_module will be "my_module"

# EXPLICIT RELATIVE IMPORTS
# - Based on __name__ and, for each ".", just remove one from the name

# IMPLICIT RELATIVE IMPORTS
# - Start, but do not include, the main script for imports, no matter how deep you are in the dir tree.
# - EX: if you are in /sub_dir/another/my_module.py and you need to import /sub_dir_2/my_module_2.py do:
#   - import sub_dir_2.my_module (notice, it is from the root, not relative to your module)

# For the script you execute from the command line, __name__ is "__main__".
# Otherwise, the __name__ is the name of the file w/o the .py extension.

# You can run a script as a module with the -m option, which will make __name__
# still be "__main__", but you can run it without the py extension and it won't
# add the directory of the executing script to sys.path

# Relative imports are based on __name__ unless __package__ is not None.
# In that case, they are based on __package__. 

# W/i the module, __package__ can be None. When imported, if the module didn't 
# set __package__ (it is None), it will be based on the __name__ (basically, everything except the thing following the last ".")

# The __name__ of an __init__.py file is the same as the package

# When a package is imported __init__.py is executed and anything it defines become properties
# of the package's namespace.

# Now, when you import tle_proj you can do tle_proj.func()
def func():
    print("I'm on the package namespace, not a module...")