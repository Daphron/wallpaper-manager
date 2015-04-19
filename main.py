from __future__ import print_function
import datetime
import os
from os import listdir
from os.path import isfile, join
import praw
import fileinput
import subprocess
import time
import random
import sys
import argparse
import reddit_scraper
VALID_FILETYPES = ("jpg", "JPG", "png", "PNG")
#TODO a master dotfile config for the user so don't need to pass all these
#parmeters each time
#TODO recursive directories for images
#TODO merge config file and currentwallpaper file

def update_images(cwd, configfile):
    files = [join(cwd,f) for f in listdir(cwd) if isfile(join(cwd,f))]
    files = ["\"" + f + "\"" for f in files if f.endswith(VALID_FILETYPES)]
    if not os.path.exists(configfile):
        with open(configfile, "w") as config:
            #create the file if it doesn't exist
            pass

    with open(configfile, "r+") as config:
        for line in config:
            if line.split(",")[0] in files:
                files.remove(line.split(",")[0])

        for filepath in files:
            config.write(filepath)
            config.write(",100," + str(time.time()) + ",false") #initial rating 100 then timestamp, then whether "checked" as a safe wallpaper
            config.write("\n")

def pick_wallpaper(configfile, starttime, endtime):
    st = datetime.datetime.strptime(starttime, "%H:%M")
    st = st.replace(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
    et = datetime.datetime.strptime(endtime, "%H:%M")
    et = et.replace(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
    wallpapers = []
    with open(configfile, "r") as config:
        for line in config:
            filepath = line.split(",")[0]
            weight = max(0, int(line.split(",")[1]))
            timestamp = float(line.split(",")[2])
            checked = line.split(",")[3] == True
            if checked or (datetime.datetime.now().weekday() in (5,6)) or not (st < datetime.datetime.now() < et):
                if timestamp < time.time():
                    wallpapers += weight * [filepath]

    print("Picked a new wallpaper")
    try:
        return random.choice(wallpapers)
    except IndexError:
        print("No wallpaper valid for viewing at this time, Exiting...")
        sys.exit(0)

def run(configfile, curr_wallpaper_file, starttime, endtime, time_between=15):
    while True:
        wallpaper = pick_wallpaper(configfile, starttime, endtime)
        subprocess.Popen('feh --bg-scale ' + wallpaper, shell=True)
        with open(curr_wallpaper_file, 'w+') as curr_file:
            curr_file.write(wallpaper)
        time.sleep(time_between)

def __vote(ammount, curr_wallpaper_file, config_file):
    curr_wallpaper = None
    with open(curr_wallpaper_file) as fin:
        curr_wallpaper = fin.readline()

    if curr_wallpaper == None:
        print("ERROR reading the current wallpaper file")
        return

    for line in fileinput.FileInput(config_file, inplace=1):
        if line.startswith(curr_wallpaper):
            weight = int(line.split(",")[1])
            weight = max(0, weight+ammount)
            print(line.split(",")[0] + "," + str(weight) + "," + ",".join(line.split(",")[2:-1]) + "," + "true")
        else:
            print(line, end="")

def upvote(ammount, curr_wallpaper_file, config_file):
    __vote(int(ammount), curr_wallpaper_file, config_file)
def downvote(ammount, curr_wallpaper_file, config_file):
    __vote(-1*int(ammount), curr_wallpaper_file, config_file)

def tired(ammount, curr_wallpaper_file, config_file):
    curr_wallpaper = None
    with open(curr_wallpaper_file) as fin:
        curr_wallpaper = fin.readline()

    if curr_wallpaper == None:
        print("ERROR reading the current wallpaper file")
        return

    for line in fileinput.FileInput(config_file, inplace=1):
        if line.startswith(curr_wallpaper):
            timestamp = line.split(",")[2]
            timestamp = float(timestamp)+float(ammount)*86400 #86400 s in day 
            print(",".join(line.split(",")[:2]) + "," + str(timestamp)) 
        else:
            print(line, end="")

def remove_from_rotation(curr_wallpaper_file, config_file):
    curr_wallpaper = None
    with open(curr_wallpaper_file) as fin:
        curr_wallpaper = fin.readline()

    if curr_wallpaper == None:
        print("ERROR reading the current wallpaper file")
        return

    for line in fileinput.FileInput(config_file, inplace=1):
        if line.startswith(curr_wallpaper):
            print(line.split(",")[0] + "," + str(0) + "," + ",".join(line.split(",")[2:]), end="")
        else:
            print(line, end="")


def download(num_images, config_file, wallpapers_dir, subreddit):
    r = praw.Reddit(user_agent="linux:wallpaper-manager:v0.7 (by /u/daphron)")
    args = argparse.Namespace()
    args.limit = num_images # num submissions to look for
    args.length = 30
    args.subreddit = subreddit 
    args.output = wallpapers_dir
    # choices=["hot", "new", "controversial", "top"], metavar="type", default="new")
    args.sort = "top" 
    args.score = 40
    args.no_nsfw = True
    args.quiet = False
    reddit_scraper.subreddit_retrieve(r, args)

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configfile', help='The config file to use')
    parser.add_argument('-u', '--update', help='Directory containing the wallpapers you wish to import')
    parser.add_argument('-r', '--run', help='Run and change wallpapers with <run> minutes between each wallpaper. MUST also set --currentwallpaper')
    parser.add_argument('-w', '--currentwallpaper', help='File that reccords what wallpaper is currently in use')
    parser.add_argument('--upvote', help='Upvote the given wallpaper this many times')
    parser.add_argument('--downvote', help='Downvote the given wallpaper this many times')
    parser.add_argument('-t', '--tired', help="Say that you are tired of this wallpaper and don't want to see it for this many days")
    parser.add_argument('-d', '--download', help="How many new reddit posts per day you want to download and add to your rotation")
    parser.add_argument('--wallpaperdir', help="Where to put newly downloaded wallpapers")
    parser.add_argument('--remove', help="Remove a file from rotation, making it never be your wallpaper again", action='store_true')
    parser.add_argument('-s', '--subreddit', help="What subreddit do you want to download from", default="wallpapers")
    parser.add_argument('--startwork', help='Start time for disabling unchecked wallpapers', default="08:30")
    parser.add_argument('--endwork', help='End time for disabling unchecked wallpapers', default="17:30")
    args = parser.parse_args()

    if not args.configfile:
        print("ERROR: Input a config file with the -c option")
        return
    if args.remove:
        remove_from_rotation(args.currentwallpaper, args.configfile)
    if args.tired:
        if not args.currentwallpaper:
            print("ERROR: Input a currentwallpaper file with the -w option")
            return
        tired(args.tired, args.currentwallpaper, args.configfile)
    if args.upvote:
        if not args.currentwallpaper:
            print("ERROR: Input a currentwallpaper file with the -w option")
            return
        upvote(args.upvote, args.currentwallpaper, args.configfile)
    if args.downvote:
        if not args.currentwallpaper:
            print("ERROR: Input a currentwallpaper file with the -w option")
            return
        downvote(args.downvote, args.currentwallpaper, args.configfile)
    if args.download:
        if args.wallpaperdir:
            download(args.download, args.configfile, args.wallpaperdir, args.subreddit)
        else:
            print("MUST RUN WITH wallpaperdir if running --update")
    if args.update:
        update_images(args.update, args.configfile)

    if args.run and not args.currentwallpaper:
        print("MUST RUN WITH currentwallpaper if also running with --run")
    if args.run and args.currentwallpaper:
        run(args.configfile, args.currentwallpaper, args.startwork, args.endwork, time_between=int(args.run))

if __name__ == "__main__":
    main(sys.argv[1:])
