import os
from os import listdir
from os.path import isfile, join
import fileinput
import subprocess
import time
import random
import sys
import argparse
VALID_FILETYPES = ("jpg", "JPG", "png", "PNG")

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
            config.write(",100") #initial rating 100
            config.write("\n")

def pick_wallpaper(configfile):
    wallpapers = []
    with open(configfile, "r") as config:
        for line in config:
            filepath = line.split(",")[0]
            weight = int(line.split(",")[1])
            wallpapers += weight * [filepath]

    print("Picked a new wallpaper")
    return random.choice(wallpapers)

def run(configfile, curr_wallpaper_file, time_between=15):
    while True:
        wallpaper = pick_wallpaper(configfile)
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
            weight = int(line.split(",")[-1])
            weight = max(0, weight+ammount)
            print(",".join(line.split(",")[:-1]) + "," + str(weight))
        else:
            print(line, end="")

def upvote(ammount, curr_wallpaper_file, config_file):
    __vote(int(ammount), curr_wallpaper_file, config_file)
def downvote(ammount, curr_wallpaper_file, config_file):
    __vote(-1*int(ammount), curr_wallpaper_file, config_file)


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configfile', help='config file to use')
    parser.add_argument('-u', '--update', help='directory to update CANT be used at same time as importdir')
    parser.add_argument('-r', '--run', help='run the program and acually change your wallpaper (MUST also have --currentwallpaper)')
    parser.add_argument('-w', '--currentwallpaper', help='the file that stores the current wallpaper filepath')
    parser.add_argument('--upvote', help='upvote the given wallpaper this many times')
    parser.add_argument('--downvote', help='downvote the given wallpaper this many times')
    args = parser.parse_args()

    if not args.configfile:
        print("ERROR: Input a config file with the -c option")
        return
    if args.upvote:
        upvote(args.upvote, args.currentwallpaper, args.configfile)
    if args.downvote:
        downvote(args.downvote, args.currentwallpaper, args.configfile)
    if args.update:
        update_images(args.update, args.configfile)

    if args.run and not args.currentwallpaper:
        print("MUST RUN WITH currentwallpaper if also running with --run")
    if args.run and args.currentwallpaper:
        run(args.configfile, args.currentwallpaper, time_between=int(args.run))

if __name__ == "__main__":
    main(sys.argv[1:])
