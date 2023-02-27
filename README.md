# nonsteamutil

<p>This is a python Utility to add a standalone Linux game or application as a non-steam game to the Steam Deck (Linux SteamOS only)</p>

<p>I wanted the functionality to add a standalone application as a non-steam game wihtout needing another application like Steam Rom Manger or BoilR.</p>

<p>This was created from scottrice's Ice and Pysteam projects, with help from CorporalQuesadilla's Steam-Shortcut-Manager as well.</p>

<p>I had to update the code for Python 3, and the functionality has been reduced to just appending a game to shortcuts.vdf</p>

<p>This utility is currently hardcoded to look for the artwork in a folder named "Steam-Artwork" that is two directories above where the utility is located.</p>
<p>The filenames of the Steam-Artwork images can be changed in config.txt.</p>
<p>The directory structure should look like this:</p>

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
