import os
import glob
import argparse
import sys
from colorama import init, Fore, Back, Style
init()

# todo
# add in arguments that take advantage of argparse
# handle weird characters, right now if it finds some weird chars in a file name it all crashes
parser = argparse.ArgumentParser()
parser.add_argument("channel_name", help="The name of channel that you want to make a comp of")
parser.add_argument("number_of_clips", help="The number of clips you want to download from that channel")
args = parser.parse_args()
# print(args.number_of_clips)
# print(args.channel_name)

print(Fore.CYAN + " _____       _ _       _         _ _    _____ _ _        _____              ")          
print("|_   _|_ _ _|_| |_ ___| |_ ___ _| | |  |     | |_|___   |     |___ _____ ___ ") 
print("  | | | | | | |  _|  _|   |___| . | |  |   --| | | . |  |   --| . |     | . |")
print("  |_| |_____|_|_| |___|_|_|   |___|_|  |_____|_|_|  _|  |_____|___|_|_|_|  _|")
print("                                                 |_|                    |_|  ")
print("Made by Net_Code#4028")

# writing out the varibles that are going to be used by twitch-dl to download the clips
channel_name = (args.channel_name) + " "
output_file_name = (args.channel_name) + "_WeeklyCompilation.mp4"
download = "--download "
number_to_download = "--limit " + (args.number_of_clips) + " "
timePeriod = "--period last_week "
clips = "clips "
# create a string named cmd that is the entire twitch-dl command that is going to be used
cmd = "twitch-dl " + clips + channel_name + timePeriod + number_to_download + download

# the function to use the cmd string to download the clips
def download_clips():
    os.system(cmd)
    # it takes 4 min to download the videos

# this lists the .mp4 files it finds in the dir its in, so the downloaded clips.  And adds their names to a file to reference later as well as keeping track of the number of lines in the file.  It then references the file to find what each clip is named and loops through that until it hits the number of lines (determined from the prior "for" loop).  At which point it edits each clip to change the timescale so all of the clips have the same timescale, which makes them concat correctly.  It also outputs the fixed clips in a new folder called "fixed_clips"
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
    for i in files_list:    # the reason for all of this garbage is becasue the ffmpeg arg -video_track_timescale does not support inputs from a file, so this writes each files name to a list and then pull from the list
        f = open("file_list1.txt", "r")
        linelist = f.readlines()
        input_file = linelist[lineNum].rstrip('\n')
        lineNum = lineNum + 1
        increment = increment + 1   # the purpose of this piece of garbage is to make sure that each fixed clip has a unique name by adding onto the end with an incrementing int which is then converted into a string and used
        new_fixed_filename = fixed_output_file_name_number + increment
        fixed_output_file_name = fixed_output_file_name + str(new_fixed_filename)
        os.system("ffmpeg -loglevel 8 -fflags +igndts -i " + input_file + " -video_track_timescale 90000 " + "fixed_clips\\" + fixed_output_file_name + ".mp4")
        print("fixed a file")
    f.close()
    print("Finished changing video timescale" + "\n")
    # it takes 2:30 min to fix the downloaded clips
# this finds each .mp4 file in the "fixed_clips" dir and write their names out to a new file 
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
    os.system("ffmpeg -loglevel 8 -f concat -safe 0 -i file_list2.txt " + output_file_name)
    print("Finished creating the compilation")
    # it takes 2 min to create the final video
# THIS MAKES EVERYTHING WORK PERFECTLY
# ffmpeg -i input1.mp4 -video_track_timescale 90000 fixed1.mp4 

# clean up the folder so that you are just left with a folder named "final" and nothing is left over to mess up the next run
def clean_up():
    os.system("move " + output_file_name + " .\\final")
    os.system("del *.mp4")
    os.system("del file_list1.txt")
    os.system("del file_list2.txt")
    os.system("del fixed_clips\\*.mp4")
    os.system("rmdir fixed_clips")
    print("Finished cleaning up")

# call the functions to download the clips, list them, concat them, and clean up
download_clips() 
list_files()
list_files2()
concat_files()
clean_up()