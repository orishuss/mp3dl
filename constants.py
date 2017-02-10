# Output audio format.
AUDIO_FORMAT = "mp3"

# Executable to download with.
DOWNLOADER = "third_party/youtube-dl/youtube_dl/__main__.py"

# Search Engine to look up song names' at.
SEARCH_ENGINE = "ytsearch" # youtube.

# File containing list of songs to download.
BATCH_FILE = "to-dl.txt"
# File containing list of songs to download - template.
BATCH_FILE_TEMPLATE = "to-dl-template.txt"
# Batch file comment character
BATCH_FILE_COMMENT_CHARACTER = "#"

# Maximum downloads simultaneously
MAXIMUM_SIMULTANEOUS_DOWNLOADS = 3