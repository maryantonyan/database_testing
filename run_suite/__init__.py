import imp
import os.path

def add_path():
    import sys
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if path not in sys.path:
        sys.path.append(path)

try:
    module_name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    imp.find_module(module_name)
except ImportError:
    add_path()