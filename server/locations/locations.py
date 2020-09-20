"""
This module is used to share the locations between the scrapers and the
web-ui applications.
"""

from dataclasses import dataclass

@dataclass
class Location:
    """ Stores location related data.
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
DATA_DIRECTORY = "../data"
