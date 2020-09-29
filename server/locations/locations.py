"""
This module is used to share the locations between the scrapers and the
web-ui applications.
"""
import os
import pathlib
from dataclasses import dataclass


@dataclass
class Location:
    """Stores location related data.
    dataclass creates an __init__ function that expects the four members.
    """

    name: str
    file_name: str
    ip_address: str
    label: str


# Adjust the values to suit your own set up.
# Note: ex must always be the first entry.
LOCATIONS = [
    Location("ex", "external", "", "External"),
    Location("s0", "downstairs-back-room", "http://192.168.2.180", "Downstairs"),
    Location("s1", "upstairs-landing", "http://192.168.2.181", "Upstairs"),
]

# Path to data directory.
# File paths to use.
__current_dir = os.path.dirname(os.path.abspath(__file__))
__path = pathlib.Path(__current_dir)
__parent_dir = __path.parent.parent
DATA_STORE_PATH = os.path.join(__parent_dir, "data")
