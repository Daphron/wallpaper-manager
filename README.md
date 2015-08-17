# wallpaper-manager
##What is it?
Wallpaper-manager is a lightweight background management program for those who enjoy variety in their wallpapers. The main goal of wallpaper-manager is to provide a pandora-like system for your favorite wallpapers so you see them more often. 

##What can it do?
* Display a rotating series of wallpapers
* Allows you to weight the likelyhood of seeing certain wallpapers by weight
* Automatically download new wallpapers from image subreddits (not currently supported/working)

##How to use
In order to display a random new wallpaper each 15 minutes run:
```
python2 main.py --configfile /path/to/wallpapers/config.txt --currentwallpaper /path/to/wallpapers/currentwallpaper.txt --run 15 --update /path/to/walpapers/
```
This will automatically create a file containing the ratings for your wallpapers and display wallpapers based on thos ratings.

You can upvote or downvote a wallpaper with
```
python2 main.py --configfile /path/to/wallpapers/config.txt --currentwallpaper /path/to/wallpapers/currentwallpaper.txt --upvote 5
```
and
```
python2 main.py --configfile /path/to/wallpapers/config.txt --currentwallpaper path/to/wallpapers/currentwallpaper.txt --downvote 5
```
The parameters for upvote and downvote can be adjusted depending on how much you like/dislike the wallpaper

You can remove the wallpaper from rotation for 30 of days with
```
python2 main.py --configfile /path/to/wallpapers/config.txt --currentwallpaper path/to/wallpapers/currentwallpaper.txt --tired 30
```
And you can permanantly remove a wallpaper from rotation with
```
python2 main.py --configfile /path/to/wallpapers/config.txt --currentwallpaper path/to/wallpapers/currentwallpaper.txt --remove
```

##Reccomendations
I reccomend that you put a background call to this program (called with --run) in your .xinitrx in order to start this automatically on startup. I also reccomend you create a few keybindings in your window manager of choice for commands such as upvote, downvote, tired, and remove.
