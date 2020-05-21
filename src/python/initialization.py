from yaml import safe_load
import os


# Read configuration file
root_dir = os.path.join(os.path.dirname(__file__), "..",  "..")
src_dir = os.path.join(root_dir, "src")
template_dir = os.path.join(root_dir, "src", "ressources", "templates")


with open(os.path.join(root_dir, "config.yml"), 'r') as stream:
    DICT_CONFIG = safe_load(stream)

