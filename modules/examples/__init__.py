"""
Initialization module for the CaDump class.

This module ensures the CaDump class is imported and sets a default value for its param3 attribute during initialization.
"""

from .ca_dump import CaDump

# Set a default value for param3 globally if required
CaDump.param3 = 1

all = ["CaDump"]  # Explicitly define what is exposed when the module is imported