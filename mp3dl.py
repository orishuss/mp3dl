import subprocess
import os
import logging
import shutil
import time

import config
import constants

def download_song(song):
	"""
	Download the given song.
	Returns the download process for the song.
	"""
	logging.info("Downloading Song {}".format(song))
	
	# Open subprocess that downloads song.
	download = subprocess.Popen(["python " + constants.DOWNLOADER,
								"--default-search", constants.SEARCH_ENGINE,
								"--extract-audio", "--audio-format", constants.AUDIO_FORMAT,
								"--ffmpeg-location", "C:\\",
								"--output", config.OUTPUT_FOLDER + song + ".%(ext)s",
								song,
								"--quiet"],
								shell=True)
					
	return download

def download_song_list(song_list):
	"""
	Download a list of songs.
	"""
	simulatenous_downloads = 0
	downloads = []
	# Download songs.
	while  (song_list): # not empty
		# Download a song if haven't reached the maximum simultaneous downloads.
		if (constants.MAXIMUM_SIMULTANEOUS_DOWNLOADS > simulatenous_downloads):
			downloads.append(download_song(song_list.pop(0)))
			simulatenous_downloads += 1

		# Poll which songs are finished.
		polls = [p.poll() for p in downloads]

		# Determine which songs have finished downloading.
		finished_downloads = [downloads.pop(i) for i in range(len(polls))[::-1] if polls[i] is not None]
		simulatenous_downloads -= len(finished_downloads)
		
		# Sleep for a bit, don't kill CPU.
		time.sleep(1)
	
	# Wait for last songs to finish
	[p.wait() for p in downloads]
	
def edit_batch_file():
	"""
	Allow the user to edit the batch file.
	"""
	# Copy template.
	shutil.copyfile(constants.BATCH_FILE_TEMPLATE, constants.BATCH_FILE)
	
	# Open the batch file for editing.
	edit_proc = subprocess.Popen(	[config.EDITOR,
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
	explorer = subprocess.Popen([config.EXPLORER,
								os.path.abspath(config.OUTPUT_FOLDER)])
								
def validate_dependencies():
	"""
	Validates that all dependencies exist.
	Returns whether they exist or not.
	"""
	if not os.path.isfile(constants.DOWNLOADER):
		logging.error(	constants.DOWNLOADER + " Doesn't exist.\n" +
						"\trun 'git submodule update --init --recursive' to download.")
		return False
		
	return True

def main():
	# Set logging to debug mode.
	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
	
	# Validate that dependencies exist.
	if validate_dependencies() is False:
		return 1
	
	# Switch to script's directory.
	script_path = os.path.abspath(__file__)
	script_dir = os.path.dirname(script_path)
	os.chdir(script_dir)
	
	# Allow the user to edit the batch file.
	edit_batch_file()
	
	# Read songs from batch file.
	with open(constants.BATCH_FILE) as f:
		songs = [x.strip() for x in f.readlines() if is_valid_song_name(x)]
	
	# Download all songs
	download_song_list(songs)
	
	# Open output folder.
	open_output_folder()

if "__main__" == __name__:
	main()