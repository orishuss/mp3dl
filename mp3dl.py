#!/usr/bin/python

import os
import logging
import webbrowser

import config
import constants
from downloader import Downloader
from batcher import Batcher

def open_output_folder():
    """
    Open the output folder.
    """
    # Open file explorer at the output folder.
    webbrowser.open(os.path.abspath(config.OUTPUT_FOLDER))
                                
def main():
    # Set logging to debug mode.
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    
    # Switch to script's directory.
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    os.chdir(script_dir)
    
    # Initiate Downloader & Batcher.
    downloader = Downloader()
    batcher = Batcher()
    
    # Validate that dependencies exist.
    if downloader.validate_dependencies() is False:
        return 1

    # Allow the user to edit the batch file, then read it.
    batcher.edit_batch_file()
    songs = batcher.read_batch_file()

    # Download all songs
    downloader.download_song_list(songs)

    # Open output folder.
    open_output_folder()

if "__main__" == __name__:
    main()