#                                         ***WAV file splitter***
#                                                Dante Rossi

# ABOUT:
# This script splits .wav files. The .wav files are read in and
# if they are longer than 1hr, they split them into 1hr wave files
# and renamed in new folder.

# The script also returns the number of files in the path and the total length of videos in path

import os
import time
import glob
from pydub import AudioSegment
from pydub.utils import make_chunks
import ntpath
import wave
import contextlib
import subprocess

#  start directory
path = 'ENTER_DIRECTORY'  # put directory of files that need to be split here
subprocess.call("explorer " + path, shell=True) # open windows explorer
files_to_check = glob.glob(path + '\\*.wav')
errors = []
num_files_split = []
#  run text
print '\n'
print 'Begin Splitting'
print '\n'
time.sleep(1)
num_files = len(files_to_check)
total_time = 0
for filename in files_to_check:
    # calculate duration of .wav files in seconds from number of frames and rate
    print('\n')
    try:
        with contextlib.closing(wave.open(filename, 'r')) as f:
            # calculate file length in seconds
            frames = f.getnframes()
            rate = f.getframerate()
            print '--File Info--'
            print 'Sample Rate:', rate, 'Hz'
            duration_sec = int(frames / float(rate))
            # conversion of file length to hr, min, & sec to display to user
            minutes, second = divmod(duration_sec, 60)
            hours, minute = divmod(minutes, 60)
            total_time += duration_sec
            # print time details of current file for user
            print('File Length: ' + str(hours) + ' hrs' + ' ' + str(minute) + ' min ' + str(second) + ' sec')
        # split all .wav files longer than 3600 seconds (1 hour) into hour long "chunks"
        if duration_sec > 3600:
            num_files -= 1
            print 'Processing:', filename, '...\n'
            myaudio = AudioSegment.from_file(filename, "wav")
            chunk_length_ms = 3600000  # 1 hour in milliseconds *pydub calculates in milliseconds*
            chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks of 1 hour
            # Export all of the individual chunks as wav files and save into new folder
            for i, chunk in enumerate(chunks):
                num_files += 1
                head, tail = ntpath.split(filename)
                name = tail
                rename = os.path.splitext(ntpath.basename(name))[0]
                chunk_name = (rename + "_" + "{0}.wav".format(i))
                print 'Exporting:', "Chunk {0}".format(i)
                newpath = (path + "\\" + "split")  # make new folder to save splits to
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                chunk_rename = os.path.join(newpath, chunk_name)
                if not os.path.exists(chunk_rename):
                    chunk.export(chunk_rename, format="wav")
                print("Chunk already exists")
            num_files_split.append(filename)
        else:
            print'Skipped:', filename, '\n'  # skip files less than 1 hour
    except:
        #  print and collect errors
        print 'Error:', filename, '\n'  # files that could not be split for whatever reason
        errors.append(filename)
# print run results
print '\n'
print '--FINISHED SPLITTING--\n', str(len(num_files_split)), 'file(s) split\n'
print str(len(errors)), 'error(s) occurred\n'
# print path report
print "Number of files in path:", num_files, '\n'
minutes, second = divmod(total_time, 60)
hours, minute = divmod(minutes, 60)
print "Total length of videos in path:", hours, "hrs", minute, "min", second, "sec", '\n'
# error report
if len(errors) > 0:
    print str(errors), 'could not be split'
