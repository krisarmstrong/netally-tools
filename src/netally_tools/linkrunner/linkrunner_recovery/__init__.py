"""LinkRunner Recovery Tool.

A utility to recover and update MAC address, serial number, and option bits
on LinkRunner Pro/Duo devices.
"""

__version__ = "2.0.1"

from .recovery import main

__all__ = ["main"]
