#!/usr/bin/python

import subprocess
import os
import logging
import shutil
import webbrowser

import config
import constants
from downloader import Downloader

def edit_batch_file():
    """
    Allow the user to edit the batch file.
    """
    # Copy template.
    shutil.copyfile(constants.BATCH_FILE_TEMPLATE, constants.BATCH_FILE)

    # Open the batch file for editing.
    edit_proc = subprocess.Popen(	[constants.EDITOR,
                                    constants.BATCH_FILE])

    # Wait for user to finish editing the file.
    return_code = edit_proc.wait()
                                
def is_valid_song_name(song_name):
    """
    Check if a song name is valid.
    """
    # Check empty name.
    if not song_name:
        return False
    # Check commented name.
    if song_name.startswith(constants.BATCH_FILE_COMMENT_CHARACTER):
        return False
    return True
    
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
    
    # Initiate downloader.
    downloader = Downloader()
    
    # Validate that dependencies exist.
    if downloader.validate_dependencies() is False:
        return 1

    # Allow the user to edit the batch file.
    edit_batch_file()

    # Read songs from batch file.
    with open(constants.BATCH_FILE) as f:
        songs = [x.strip() for x in f.readlines() if is_valid_song_name(x)]

    # Download all songs
    downloader.download_song_list(songs)

    # Open output folder.
    open_output_folder()

if "__main__" == __name__:
    main()