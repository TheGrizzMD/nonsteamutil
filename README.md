# nonsteamutil

This is a python utility to add a standalone game or application as a non-steam game to Steam within SteamOS for the Steam Deck (Does not work with Windows).  

I wanted the functionality to add a standalone application as a non-steam game without the need for another application like Steam Rom Manger or BoilR.  

Most of the code is from [scottrice](https://github.com/scottrice)'s [Pysteam](https://github.com/scottrice/pysteam) and [Ice](https://github.com/scottrice/Ice)   projects, with a small part from [CorporalQuesadilla](https://github.com/CorporalQuesadilla)'s [Steam-Shortcut-Manager](https://github.com/CorporalQuesadilla/Steam-Shortcut-Manager) as well to increment the AppID.  

I had to update the code for Python 3, and the functionality has been reduced to just appending a game to shortcuts.vdf due to my limited knowledge of Python. 

# File Structure

This utility is currently hardcoded to look for the Steam artwork in a folder named "Steam-Artwork" that is two directories above where the utility is located.  

The filenames of the Steam-Artwork images can be changed in the config file.  

The directory structure should look like this:  

    Application Directory
        /utils
            /nonsteamutil
                 /config.txt
        /Steam-Artwork
            /icon.png
            /lastplayed.png
            /hero.png
            /logo.png
            /portrait.png

# Changing the Configuration
The [GAME] section of the config.txt file is all that needs to be modified.

The utility is going to assume that the "Game Exe" is in the "Application Directory" (see the directory structure example in the section above.)

There is also a command line option to specify a different config file to use.

# Example Usage within a shell script:

    #!/bin/bash
    cd utils/nonsteamutil
    konsole --noclose -e python nonsteamutil.py --config config.txt

# Backups

The utility will backup the shortcuts.vdf file in the Backups folder in case the utility screws up the shortcuts.vdf file when adding a game.

# Spaghetti Code Disclaimer

The code is very messy. I stopped working on it once it produced the functionality that I wanted, but I am making it available for the small chance that it helps someone else.
