from ww import f as fstr
import os
import time 

class NodeException(Exception):
  pass

def confirm_file(path):
  if not os.path.isfile(path):
    raise NodeException( fstr("Required file does not exist: {path}") )

def confirm_dir(path):
  if not os.path.isdir(path):
    raise NodeException( fstr("Required directory does not exist: {path}") )