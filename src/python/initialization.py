from yaml import safe_load
import os


# Read configuration file
this_dir = os.path.dirname(__file__)
with open(os.path.join(this_dir, "../..", "config.yml"), 'r') as stream:
    DICT_CONFIG = safe_load(stream)

