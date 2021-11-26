import os
import glob
import argparse
import sys
from colorama import init, Fore, Back, Style
from itertools import cycle
import time
import threading
from halo import Halo
import re
init()

parser = argparse.ArgumentParser()
parser.add_argument("channel_name", help="The name of channel that you want to make a comp of")
parser.add_argument("number_of_clips", help="The number of clips you want to download from that channel")
parser.add_argument("upload", help="Upload the video when its done, if you want the video uploaded use \"true or True\"")
args = parser.parse_args()

print(Fore.CYAN + " _____       _ _       _         _ _    _____ _ _        _____               ")
print(Fore.CYAN + "|_   _|_ _ _|_| |_ ___| |_ ___ _| | |  |     | |_|___   |     |___ _____ ___ ")
print(Fore.CYAN + "  | | | | | | |  _|  _|   |___| . | |  |   --| | | . |  |   --| . |     | . |")
print(Fore.CYAN + "  |_| |_____|_|_| |___|_|_|   |___|_|  |_____|_|_|  _|  |_____|___|_|_|_|  _|")
print(Fore.CYAN + "                                                 |_|                    |_|  ")
print(Fore.CYAN + "Made by Net_Code#4028" +"\n")

# writing out the varibles that are going to be used by twitch-dl to download the clips
channel_name = (args.channel_name) + " "
output_file_name = (args.channel_name) + "_WeeklyCompilation.mp4"
download = "--download "
number_to_download = "--limit " + (args.number_of_clips) + " "
timePeriod = "--period last_week "
clips = "clips "
title = channel_name+"Weekly Clip Compilation \n"
description = "These clips were taken from twitch.tv/"+channel_name+"in the last week \n"
print("Title: " + title)
print("Description: " + description)
upload_tf = False
if ((args.upload == "true") | (args.upload == "True")):
    upload_tf = True 

os.system("del video_info.txt")
with open("video_info.txt","a") as o:
    o.write(title)
    o.write(description)

# create a string named clip_dl_cmd that is the entire twitch-dl command that is going to be used
clip_dl_cmd = "twitch-dl " + clips + channel_name + timePeriod + number_to_download + download

video_title = (args.channel_name)+" Weekly Clips Compilation"
video_path = output_file_name

def edit_conf_file(input_string):
    with open("config.conf","a") as o:
        input_string = input_string + "\n"
        o.write(input_string)


# the function to use the clip_dl_cmd string to download the clips
def download_clips():
    os.system(clip_dl_cmd)
    # it takes about 4 min to download 8 clips and I"m not sure what res they were

# this lists the .mp4 files it finds in the dir its in, so the downloaded clips.  And adds their names to a file to reference later as well as keeping track of the number of lines in the file.  It then references the file to find what each clip is named and loops through that until it hits the number of lines (determined from the prior "for" loop).  At which point it edits each clip to change the timescale so all of the clips have the same timescale, which makes them concat correctly.  It also outputs the fixed clips in a new folder called "fixed_clips"
def list_files():
    dir = "."
    files_list = glob.glob(os.path.join(dir, "*.mp4"))
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
    fixed_output_file_name = "fixed_clip_0"
    lineNum = 0
    increment = 0
    for i in files_list:    # the reason for all of this garbage is becasue the ffmpeg arg -video_track_timescale does not support inputs from a file, so this writes each files name to a list and then pulls from the list
        spinner = Halo(text="Fixing files \n", spinner="dots2")    #adds the nice spinner to show that the script is doing something 
        spinner.start() #starts the nice spinner
        f = open("file_list1.txt", "r")
        linelist = f.readlines()
        input_file = linelist[lineNum].rstrip("\n")
        lineNum = lineNum + 1
        increment = increment + 1   # the purpose of this piece of garbage is to make sure that each fixed clip has a unique name by adding onto the end with an incrementing int which is then converted into a string and used
        new_fixed_filename = fixed_output_file_name[0:11] + str(increment)
        print(" "+new_fixed_filename)
        os.system("ffmpeg -hwaccel cuda -loglevel 8 -y -fflags +igndts -i " + input_file + " -video_track_timescale 90000 " + "fixed_clips\\" + new_fixed_filename + ".mp4")
        spinner.stop()  #stop the nicer spinner
    f.close()
    print("Finished changing video timescale \n")
    # it takes about 2:30 min to fix the downloaded clips
# this finds each .mp4 file in the "fixed_clips" dir and writes their names out to a new file 
def list_files2():
    dir = ".\\fixed_clips\\"
    files_list = glob.glob(os.path.join(dir, "*.mp4"))
    files_string = ""
    for i in files_list:
        files_string=files_string+"file \""+i+"\""+"\n"
    with open("file_list2.txt","a") as o:
        o.write(files_string)

# this takes all of the files listed in file_list2.txt and concats them
def concat_files():
    spinner = Halo(text="Creating the final output", spinner="dots2")
    spinner.start()
    os.system("ffmpeg -loglevel 8 -f concat -safe 0 -i file_list2.txt " + output_file_name)
    print("Finished creating the compilation")
    spinner.stop()
    # it takes about 2 min to create the final video
# THIS MAKES EVERYTHING WORK PERFECTLY
# ffmpeg -i input1.mp4 -video_track_timescale 90000 fixed1.mp4 

# clean up the folder so that there is nothing to mess up the next time your run the script
def clean_up():
    os.system("del Upload\\*.mp4")
    os.system("move " + output_file_name + " .\\Upload")
    os.system("del *.mp4")
    os.system("del file_list1.txt")
    os.system("del file_list2.txt")
    os.system("del fixed_clips\\*.mp4")
    os.system("rmdir fixed_clips")
    print(Fore.CYAN + "Finished cleaning up")

def upload_video():
    video_upload_cmd = "py video_upload.py"
    os.system(video_upload_cmd)

# this whole deal is for checking for a config file, and if it cannot find one it makes a new one
def config():
    dir = "."
    files_list = glob.glob(os.path.join(dir, "*.txt"))
    files_string = ""
    number_of_lines = 0
    config_increment = 0

    for i in files_list:
        istring = str(i)
        x = re.search("config.txt", istring)
        if x:
            lineNum = 0
            increment = 0
            for i in files_list:
                istring = str(i)
                x = re.search(channel_name, istring)

                f = open("file_list1.txt", "r")
                linelist = f.readlines()
                input_file = linelist[lineNum].rstrip("\n")
                # print(input_file)
                lineNum = lineNum + 1
            f.close()


            print("found config.txt")
            
            with open("config.txt","a") as o:
                output_string = str(config_increment) + " "
                o.write(channel_name+"\n")
                o.write(output_string+"\n")
        else:
            # create a new config file
            with open("config.txt","a") as o:
                output_string = "0"
                # o.write(output_string)

# call the functions to download the clips, list them, concat them, and clean up
# download_clips() 
# list_files()
# list_files2()
concat_files()
# clean_up()
# if (upload_tf == True):
#     upload_video()
# config()