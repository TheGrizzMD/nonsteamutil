# encoding: utf-8
"""
_shortcut_parser.py

Created by Scott on 2013-12-29.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import re

from pysteam.model import Shortcut


class ShortcutParser(object):

    def parse(self, path, require_exists=False):
        if not os.path.exists(path):
            if not require_exists:
                return []
            raise IOError("Shortcuts file '%s' does not exist" % path)

#        file_contents = open(path, "r", encoding="ISO-8859-1").read()
        file_contents = open(path, "rb").read()
#        print("Printing contents of shortcuts.vdf:")
#        print(file_contents)
#        print(file_contents.hex())
        return self.match_base(file_contents)

    def match_base(self, byte):
#        match = re.match(r"\u0000shortcuts\u0000(.*)\u0008\u0008$", string, re.IGNORECASE)
        match = re.match(b'\x00shortcuts\x00(.*)\x08\x08$', byte)
#        print("printing match:")
#        print(match)
        if match:
            return self.match_array_string(match.groups()[0])
        else:
            return None

    def match_array_string(self, byte):
#        print(byte)
        # Match backwards (aka match last item first)
        if byte == "":
            return []
        # One side effect of matching this way is we are throwing away the
        # array index. I dont think that it is that important though, so I am
        # ignoring it for now
        shortcuts = []
        while True:
#            match = re.match(r"(.*)\u0000[0-9]+\u0000(\u0001AppName.*)\u0008", byte, re.IGNORECASE)
            match = re.match(b'(.*)\x00[0-9]+\x00(\x01AppName.*)\x08', byte, re.IGNORECASE)
#            print("printing match app:")
#            print(match)
            if match:
                groups = match.groups()
                byte = groups[0]
                shortcuts.append(self.match_shortcut_string(groups[1]))
            else:
                shortcuts.reverse()
                return shortcuts

    def match_shortcut_string(self, byte):
        # I am going to cheat a little here. I am going to match specifically
        # for the shortcut string (Appname, Exe, StartDir, etc), as oppposed
        # to matching for general Key-Value pairs. This could possibly create a
        # lot of work for me later, but for now it will get the job done
        match = re.match(
            r"\u0001AppName\u0000(.*)\u0000\u0001Exe\u0000(.*)\u0000\u0001StartDir\u0000(.*)\u0000\u0001icon\u0000(.*)\u0000\u0000tags\u0000(.*)\u0008",
            byte, re.IGNORECASE)
        if match:
            # The 'groups' that are returned by the match should be the data
            # contained in the file. Now just make a Shortcut out of that data
            groups = match.groups()
            appname = groups[0]
            exe = groups[1]
            startdir = groups[2]
            icon = groups[3]
            tags = self.match_tags_string(groups[4])
            return Shortcut(appname, exe, startdir, icon, tags)
        else:
            return None

    def match_tags_string(self, byte):
        tags = []
        while True:
            match = re.match(r"(.*)\u0001[0-9]+\u0000(.*?)\u0000", byte)
            if match:
                groups = match.groups()
                byte = groups[0]
                tag = groups[1]
                tags.append(tag)
            else:
                tags.reverse()
                return tags
