"""
This module is used to share the locations between the scrapers and the
web-ui applications.
"""

from dataclasses import dataclass

@dataclass
class Location:
    """ Stores location related data. """
    name: str
    ip_address: str
    label: str


# Adjust the values to suit your own set up.
# Note: ex must always be the first entry.
LOCATIONS = [
    Location("ex", "", "External"),
    Location("s0", "http://192.168.2.180", "Downstairs"),
    Location("s1", "http://192.168.2.181", "Upstairs"),
]
