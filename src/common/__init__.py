from . import constants
from . import helper
from . import test_helper

import os

__all__ = [
    "constants",
    "helper",
    "test_helper",
]

# check if the yearly_data_dir exists or not.
if(not os.path.isdir(constants.YEARLY_DATA_DIR)):
    print(f"common/__init__.py: YEARLY_DATA_DIR: [{constants.YEARLY_DATA_DIR}]\
          does not exist. Creating . . . ")
    # If not create it
    try:
        os.mkdir(constants.YEARLY_DATA_DIR)
        print(f"common/__init__.py: Created YEARLY_DATA_DIR: \
              [{constants.YEARLY_DATA_DIR}]")
    except OSError as error:
        print(f"common/__init__.py: Error Creating YEARLY_DATA_DIR:\
              [{constants.YEARLY_DATA_DIR}]")

