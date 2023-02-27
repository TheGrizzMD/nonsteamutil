# encoding: utf-8

# from ice.parsing.rom_parser import ROMParser
# from rom_finder import ROMFinder
from tasks.steam import LaunchSteamTask
from tasks.logging import LogAppStateTask
from tasks.environment import PrepareEnvironmentTask
from tasks.shortcuts import SyncShortcutsTask
from tasks.grid import UpdateGridImagesTask


class TaskCoordinator(object):

    def __init__(self, filesystem):
        self.filesystem = filesystem

        #I Think we are getting the list of roms here?
#        self.rom_finder = ROMFinder(self.filesystem, ROMParser())

    def tasks_for_options(self, launch_steam=False, skip_steam_check=False):
        tasks = [
            PrepareEnvironmentTask(self.filesystem, skip_steam_check),
            LogAppStateTask(),
            #removing self.rom_finder here as I believe it is just passing the rom list to SyncShortcuts task:
#            SyncShortcutsTask(self.rom_finder),
            SyncShortcutsTask(),
        ]

        if launch_steam:
            tasks = tasks + [LaunchSteamTask()]

        #Also removing self.rom_finder from UpdateGridImagesTask below as we just need parameters from config file
#        tasks = tasks + [UpdateGridImagesTask(self.rom_finder)]
#        tasks = tasks + [UpdateGridImagesTask()]
        return tasks
