from os import listdir
from os.path import isfile, join
import sys
import argparse
VALID_FILETYPES = ("jpg", "JPG", "png", "PNG")

def update_images(cwd, configfile):
    files = [join(cwd,f) for f in listdir(cwd) if isfile(join(cwd,f))]
    files = ["\"" + f + "\"" for f in files if f.endswith(VALID_FILETYPES)]
    with open(configfile, "w") as config:
        pass
    with open(configfile, "r+") as config:
        for line in config:
            if line.split(",")[0] in files:
                files.remove(line.split(",")[0])

        for filepath in files:
            config.write(filepath)
            config.write(",1") #initial rating 1
            config.write("\n")

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configfile', help='config file to use')
    parser.add_argument('-u', '--update', help='directory to update CANT be used at same time as importdir')
    args = parser.parse_args()

    if not args.configfile:
        print("Input a config file with the -c option")
        return

    if args.update:
        update_images(args.update, args.configfile)

if __name__ == "__main__":
    main(sys.argv[1:])
