#!/usr/bin/env python
# encoding: utf-8

import backups
import history
import paths
from logs import logger
from steam_shortcut_synchronizer import SteamShortcutSynchronizer


class SyncShortcutsTask(object):

#    def __init__(self, rom_finder):
#    def __init__(self):
        #removing this as we don't need roms
#        self.rom_finder = rom_finder

    def __call__(self, app_settings, users, dry_run):
        #don't need roms
#        roms = self.rom_finder.roms_for_consoles(
#            app_settings.config,
#            app_settings.consoles,
#        )

        managed_rom_archive = history.ManagedROMArchive(paths.archive_path())

        shortcut_synchronizer = SteamShortcutSynchronizer(app_settings.config, managed_rom_archive)

        for user in users:
            if dry_run:
                logger.debug("Not creating backup because its a dry run")
            else:
                logger.info("::Backing up shortcuts for U:%s" % user.user_id)
                backups.create_backup_of_shortcuts(app_settings.config, user)

            logger.info("::Syncing Shortcuts for U:%s" % user.user_id)
#            shortcut_synchronizer.sync_roms_for_user(user, roms, app_settings.consoles, dry_run=dry_run)
            shortcut_synchronizer.sync_roms_for_user(user, app_settings, dry_run=dry_run)
