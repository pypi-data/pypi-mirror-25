import os

# PATH constants
ENOS_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
PROVIDER_DIR = os.path.join(ENOS_PATH, "provider")
ANSIBLE_DIR = os.path.join(ENOS_PATH, "ansible")
SYMLINK_NAME = "current"
# SYMLINK_PATH = os.path.abspath(os.path.join(os.getcwd(), SYMLINK_NAME))
