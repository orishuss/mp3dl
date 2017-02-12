import platform
import os

OPERATING_SYSTEM = platform.system()

# The system's 'which' command to find executables in path.
SYSTEM_WHICH_COMMAND = "where" if OPERATING_SYSTEM == "Windows" else "which"