# encoding: utf-8
"""
_shortcut_parser.py

Created by Scott on 2013-12-29.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import re
from pysteam import paths
from pysteam._crc_algorithms import Crc

from pysteam.model import Shortcut


def read_shortcuts(path):
    return ShortcutSlicer().parse(path)


def write_shortcuts(path, shortcuts):
    vdf_contents = shortcuts
    with open(path, "wb") as f:
        f.write(vdf_contents)


def get_shortcuts_append(user_context):
    return read_shortcuts(paths.shortcuts_path(user_context))


def set_shortcuts(user_context, shortcuts):
    write_shortcuts(paths.shortcuts_path(user_context), shortcuts)


def shortcut_app_id_short(game_name, exe_path):
    """
  Generates the app id for a given shortcut. Steam uses app ids as a unique
  identifier for games, but since shortcuts dont have a canonical serverside
  representation they need to be generated on the fly. The important part
  about this function is that it will generate the same app id as Steam does
  for a given shortcut
  """
    algorithm = Crc(width=32, poly=0x04C11DB7, reflect_in=True, xor_in=0xffffffff, reflect_out=True, xor_out=0xffffffff)
    crc_input = ''.join([game_name, exe_path])
    high_32 = algorithm.bit_by_bit(crc_input) | 0x80000000
    return str(high_32)


def findLastEntryNumberAndPosition(path):
    # From the end, search backwards to the beginning of the last entry to get it's ID
    foundChars = 1
#    target = '\x00\x02appid'
    target = [0, 2, 97, 112, 112, 105, 100]
    print("length of target", len(target))
    lookingfor = 'target'
    lastEntryNumber = ''

    fileContents = bytearray(path)
    print("length of shortcut", len(fileContents))
    if len(fileContents) == 11:
        print("shortcut file is new so setting entry ID to 1")
        lastEntryNumber=1
    else:
        for i in range(len(fileContents)):
            if lookingfor == 'target':
#                print("file contents weird thing", fileContents[-i])
                if (fileContents[-i]) == target[-foundChars]:
                    # print(repr(target[-foundChars]) + " found")
                    foundChars = foundChars + 1
                    if foundChars > len(target):
                        lookingfor = 'number'
                else:
                    foundChars = 1
                    # make sure current character didn't 'restart' the pattern
                    # yeah I know copy-paste code sucks
                    if (fileContents[-i]) == target[-foundChars]:
                        # print(repr(target[-foundChars]) + " found")
                        foundChars = foundChars + 1
                        if foundChars > len(target):
                            lookingfor = 'number'
            else:
#                print("hopefully this is decimal value of entryid?", fileContents[-i])
                lastEntryNumber=fileContents[-i]
#               print(lastEntryNumber)
                break
#               if (fileContents[-i]).isdigit():
#                   print(repr(fileContents[-i]) + " found")
#                   lastEntryNumber = str((fileContents[-i])) + str(lastEntryNumber)
#               else:
#                    break
    # Although unnecessary, also return the character position of the last entry's ID
    print("last entry id in decimal:", lastEntryNumber)
    return lastEntryNumber


class ShortcutSlicer(object):

    def parse(self, path, require_exists=False):
        if not os.path.exists(path):
            if not require_exists:
                return []
            raise IOError("Shortcuts file '%s' does not exist" % path)

        #        file_contents = open(path, "r", encoding="ISO-8859-1").read()
        file_contents = open(path, "rb").read()
#        print("Printing contents of shortcuts.vdf:")
#        print(type(file_contents))
#        print(file_contents)
#        print(file_contents.hex())
        #Return raw shortcuts vdf as bytes type after slicing off last 2 bytes:
#        print(file_contents[:-2])
        return file_contents[:-2]


