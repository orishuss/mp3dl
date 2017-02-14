#!/usr/bin/python

from __future__ import unicode_literals # For youtube-dl
import logging
import os
import subprocess
import time
import threading
import importlib
import sys

import constants
import config

class Downloader(object):
    """
    Provides an API that downloads songs from YouTube,
    using the library youtube-dl.
    """
    # Output audio format.
    AUDIO_FORMAT = "mp3"

    # Executable to download with.
    DOWNLOADER = ["third_party", "youtube-dl", "youtube_dl"]

    # Search Engine to look up song names' at.
    SEARCH_ENGINE = "ytsearch" # youtube.

    # Maximum downloads simultaneously
    MAXIMUM_SIMULTANEOUS_DOWNLOADS = 3

    # Video to Audio converter.
    VIDEO_TO_AUDIO_CONVERTER = ["ffmpeg", "ffprobe"]
    VIDEO_TO_AUDIO_CONVERTER_DOWNLOAD_URL = "http://ffmpeg.org/download.html"

    def __init__(self):
        # Import downloader file.
        sys.path.append(os.path.join(*self.DOWNLOADER[:-1]))
        self.downloader_module = importlib.import_module(self.DOWNLOADER[-1])

    def download_song(self, song):
        """
        Download the given song.
        """ 
        logging.info("Downloading Song \'{}\'".format(song))
        
        # Youtube-DL Options may be found in the packagkes YoutubeDL.py file.
        ydl_opts = {
            "writethumbnail": True,
            "default_search": self.SEARCH_ENGINE,
            "postprocessors": [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3'
                },
                {
                'key': 'EmbedThumbnail'
                }],
            "outtmpl": os.path.join(*[config.OUTPUT_FOLDER, "%(title)s.%(ext)s"]),
            "quiet": True
            }
        # Download the song.
        with self.downloader_module.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song])

    def download_song_list(self, song_list):
        """
        Download a list of songs.
        """
        simulatenous_downloads = 0
        downloads = []
        # Download songs.
        while  (song_list): # not empty
            # Download a song if haven't reached the maximum simultaneous downloads.
            if (self.MAXIMUM_SIMULTANEOUS_DOWNLOADS > simulatenous_downloads):
                download = threading.Thread(target=self.download_song, args=([song_list.pop(0)]))
                downloads.append(download)
                download.start()
                simulatenous_downloads += 1

            # Poll which songs are finished.
            polls = [p.is_alive() for p in downloads]

            # Determine which songs have finished downloading.
            finished_downloads = [downloads.pop(i) for i in range(len(polls))[::-1] if polls[i] is False]
            simulatenous_downloads -= len(finished_downloads)

            # Sleep for a bit, don't kill CPU.
            time.sleep(1)

        # Wait for last songs to finish
        [p.join() for p in downloads]

    def validate_dependencies(self):
        """
        Validates that all dependencies exist.
        Returns whether they exist or not.
        """
        # Check that downloader script exists.
        if not os.path.exists(os.path.join(*self.DOWNLOADER)):
            logging.error(	"\t" + os.path.join(*self.DOWNLOADER) + " Doesn't exist.\n" +
                            "\trun 'git submodule update --init --recursive' to download.")
            return False
        
        # Check if all video to audio converter dependencies exist.
        where_cmds = [subprocess.Popen(
            [constants.SYSTEM_WHICH_COMMAND, 
            bin],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True) for bin in self.VIDEO_TO_AUDIO_CONVERTER]
        # Check whether any of the binaries don't exists
        video_to_audio_converter_exists = not any([p.wait() for p in where_cmds])
        
        if False == video_to_audio_converter_exists:
            logging.error(	"\tOne or more of the following don't exist:\n" +
                            "\t-\t" +
                            '\n\t-\t'.join(self.VIDEO_TO_AUDIO_CONVERTER) +
                            "\n\tDownload the package from " + self.VIDEO_TO_AUDIO_CONVERTER_DOWNLOAD_URL +
                            "\n\tAnd insert it to your system's path.")
            webbrowser.open(self.VIDEO_TO_AUDIO_CONVERTER_DOWNLOAD_URL)
            return False

        return True