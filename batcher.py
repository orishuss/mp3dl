#!/usr/bin/python

import subprocess
import os
import logging

import constants

class Batcher(object):
    """
    Takes care of reading and writing to the batch file,
    which the user uses to declare the songs he wants to download.
    """
    # File containing list of songs to download.
    BATCH_FILE = "to-dl.txt"

    # Batch file comment character
    BATCH_FILE_COMMENT_CHARACTER = "#"

    # The system's editor
    EDITOR = "notepad" if constants.OPERATING_SYSTEM == "Windows" else os.getenv('EDITOR')
    
    def __init__(self):
        # The batch file's template
        self.BATCH_FILE_TEMPLATE = os.linesep.join([
            self.BATCH_FILE_COMMENT_CHARACTER + " This file lists the songs that will be downloaded.",
            self.BATCH_FILE_COMMENT_CHARACTER + " Add songs below, save and exit when finished.",
            self.BATCH_FILE_COMMENT_CHARACTER + " Lines starting with '{}' will be ignored."
                .format(self.BATCH_FILE_COMMENT_CHARACTER)])

    def _is_valid_song_name(self, song_name):
        """
        Check if a song name is valid.
        """
        # Check empty name.
        if not song_name:
            return False
        # Check commented name.
        if song_name.startswith(self.BATCH_FILE_COMMENT_CHARACTER):
            return False
        return True
    
    def edit_batch_file(self):
        """
        Allow the user to edit the batch file.
        """
        # Write template to file.
        with open(self.BATCH_FILE, 'w') as f:
            f.write(self.BATCH_FILE_TEMPLATE)
            f.truncate()

        # Open the batch file for editing.
        logging.info("Opening batch file with " + str(self.EDITOR) + ".")
        edit_proc = subprocess.Popen(   [self.EDITOR,
                                        self.BATCH_FILE])

        # Wait for user to finish editing the file.
        return_code = edit_proc.wait()
        
    def read_batch_file(self):
        """
        Purpose:    Read a song list from the batch file and return it.
        Remarks:    Ignores lines starting with the comment character.
        """
        with open(self.BATCH_FILE) as f:
            songs = [x.strip() for x in f.readlines() if self._is_valid_song_name(x)]
            
        return songs
