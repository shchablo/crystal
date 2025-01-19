"""
Initialization module for core components of the CRYSTAL framework.

This module imports and exposes key classes for managing the core logic, parsing commands, handling configurations, and registering commands.
"""

from .ca_configurator import CaConfigurator
CaConfigurator.default_path = "/absolute/path/to/your/def.json"