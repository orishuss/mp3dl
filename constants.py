import platform
import os

OPERATING_SYSTEM = platform.system()


# File containing list of songs to download.
BATCH_FILE = "to-dl.txt"
# File containing list of songs to download - template.
BATCH_FILE_TEMPLATE = "to-dl-template.txt"
# Batch file comment character
BATCH_FILE_COMMENT_CHARACTER = "#"

# The system's 'which' command to find executables in path.
SYSTEM_WHICH_COMMAND = "where" if OPERATING_SYSTEM == "Windows" else "which"

# The system's editor
EDITOR = "notepad" if OPERATING_SYSTEM == "Windows" else os.getenv('EDITOR')