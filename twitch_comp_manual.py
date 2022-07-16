import os
import glob
import argparse
import sys
from colorama import init, Fore, Back, Style
from itertools import cycle
import time
import threading
from halo import Halo
init()

# todo
# handle weird characters, right now if it finds some weird chars in a file name it all crashes

print(Fore.CYAN + " _____       _ _       _         _ _    _____ _ _        _____               ")
print(Fore.CYAN + "|_   _|_ _ _|_| |_ ___| |_ ___ _| | |  |     | |_|___   |     |___ _____ ___ ") 
print(Fore.CYAN + "  | | | | | | |  _|  _|   |___| . | |  |   --| | | . |  |   --| . |     | . |")
print(Fore.CYAN + "  |_| |_____|_|_| |___|_|_|   |___|_|  |_____|_|_|  _|  |_____|___|_|_|_|  _|")
print(Fore.CYAN + "                                                 |_|                    |_|  ")
print(Fore.CYAN + "Made by Net_Code#4028" +"\n")
print(Fore.CYAN + "This is the manual version where you give it a file with slugs for each clip")

# writing out the varibles that are going to be used by twitch-dl to download the clips
output_file_name = "Final_Compilation.mp4"
download = "download "
quality = "-q source "
# create a string named cmd that is the entire twitch-dl command that is going to be used
cmd = "twitch-dl " + download + quality
video_path = output_file_name


# the function to use the cmd string to download the clips
def download_clips(input_slug):
    os.system(cmd + input_slug)

# this lists the .mp4 files it finds in the dir its in, so the downloaded clips.  
# And adds their names to a file to reference later as well as keeping track of the number of lines in the file.  
# It then references the file to find what each clip is named and loops through that until it hits the number of lines (determined from the prior "for" loop).  
# At which point it edits each clip to change the timescale so all of the clips have the same timescale, which makes them concat correctly.  
# It also outputs the fixed clips in a new folder called "fixed_clips"
def list_files():
    dir = '.'
    files_list = glob.glob(os.path.join(dir, '*.mp4'))
    files_string = ""
    number_of_lines = 0
    for i in files_list:
        files_string=files_string+i+"\n"
        number_of_lines = number_of_lines + 1
        # print(number_of_lines)
    with open("file_list1.txt","a") as o:
        o.write(files_string)

    os.system("mkdir fixed_clips")
    fixed_output_file_name_number = 0
    fixed_output_file_name = "fixed_clip_"
    lineNum = 0
    increment = 0
    for i in files_list:    # the reason for all of this garbage is becasue the ffmpeg arg -video_track_timescale does not support inputs from a file, so this writes each files name to a list and then pulls from the list
        spinner = Halo(text='Fixing files', spinner='dots2')
        spinner.start()
        f = open("file_list1.txt", "r")
        linelist = f.readlines()
        input_file = linelist[lineNum].rstrip('\n')
        lineNum = lineNum + 1
        increment = increment + 1   # the purpose of this piece of garbage is to make sure that each fixed clip has a unique name by adding onto the end with an incrementing int which is then converted into a string and used
        new_fixed_filename = fixed_output_file_name_number + increment
        fixed_output_file_name = fixed_output_file_name + str(new_fixed_filename)
        os.system("ffmpeg -hwaccel cuda -loglevel 8 -fflags +igndts -i " + input_file + " -video_track_timescale 90000 " + "fixed_clips\\" + fixed_output_file_name + ".mp4")
        spinner.stop()
    f.close()
    print("Finished changing video timescale" + "\n")
# this finds each .mp4 file in the "fixed_clips" dir and writes their names out to a new file 
def list_files2():
    dir = '.\\fixed_clips\\'
    files_list = glob.glob(os.path.join(dir, '*.mp4'))
    files_string = ""
    for i in files_list:
        files_string=files_string+"file \'"+i+"\'"+"\n"
    with open("file_list2.txt","a") as o:
        o.write(files_string)

# this takes all of the files listed in file_list2.txt and concats them
def concat_files():
    spinner = Halo(text='Creating the final output', spinner='dots2')
    spinner.start()
    os.system("ffmpeg -hwaccel cuda -loglevel 8 -f concat -safe 0 -i file_list2.txt " + output_file_name)
    print("Finished creating the compilation")
    spinner.stop()

# THIS MAKES EVERYTHING WORK PERFECTLY
# ffmpeg -i input1.mp4 -video_track_timescale 90000 fixed1.mp4 

# clean up the folder so that you are just left with a folder named "final" and nothing is left over to mess up the next run
def clean_up():
    os.system("move " + output_file_name + " .\\upload\\")
    os.system("del *.mp4")
    os.system("del file_list1.txt")
    os.system("del file_list2.txt")
    os.system("del fixed_clips\\*.mp4")
    os.system("rmdir fixed_clips")
    print(Fore.CYAN + "Finished cleaning up")



# call the functions to download the clips, list them, concat them, and clean up
clean_up()
# download_clips() 

f = open("slugs.txt", "r")
linelist = f.readlines()
# input_file = linelist.rstrip('\n')
input_file = linelist
for line in input_file:
    download_clips(line)
f.close()
os.system("mkdir upload\\")
list_files()
list_files2()
concat_files()
clean_up()
# upload_video()