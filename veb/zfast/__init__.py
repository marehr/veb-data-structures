import os
import sys

# load binary_tree
path = os.path.abspath('vendor/')

if path not in sys.path:
  sys.path.append(path)

del path
