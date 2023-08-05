"""Placeholder pending proper publication of DNF Python API"""
__version__ = "0.0.1"

import warnings

warning_msg = """\
The DNF Python API is not currently available via PyPI.

Please install it with your distro package manager (typically called
'python2-dnf' or 'python3-dnf'), and ensure that any virtual environments
needing the API are configured to be able to see the system site packages
directory.
"""

warnings.warn(warning_msg)