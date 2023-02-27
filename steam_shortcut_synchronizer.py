from pysteam import shortcuts
from pysteam import model
from pathlib import Path

#import roms

#from consoles import console_roms_directory
from logs import logger

from pysteam import _shortcut_appender
from pysteam import paths
import shutil

from error.env_checker_error import EnvCheckerError


# noinspection PyStatementEffect
class SteamShortcutSynchronizer(object):

    def __init__(self, config, managed_rom_archive):
        self.config = config
        self.managed_rom_archive = managed_rom_archive

#    def _guess_whether_shortcut_is_managed_by_ice(self, shortcut, consoles):
        # Helper function which guesses whether the shortcut was added during a
        # previous run of Ice with its console set as `console`. We do this the
        # same way we did before we had the flag tag, we check the console's
        # ROMs directory and see if it shows up in the executable for the shortcut
#        def shortcut_is_managed_by_console(console):
#            return console_roms_directory(self.config, console) in shortcut.exe

#        return any(map(shortcut_is_managed_by_console, consoles))

#    def shortcut_is_managed_by_ice(self, managed_ids, shortcut, consoles):
        # LEGACY: At one point I added ICE_FLAG_TAG to every shortcut Ice made.
        # That was a terrible idea, the managed_ids is a much better system. I
        # keep this check around for legacy reasons though.
#        if roms.ICE_FLAG_TAG in shortcut.tags:
#            return True
        # LEGACY: For most of Ice's life it guessed whether it managed a shortcut
        # or not. This was REALLY bad, as it was very dependent on configuration
        # and caused really strange bugs where moving directories would cause ROMs
        # to get duplicated and all sorts of bad stuff.
        #
        # Luckily, we have a history now and don't have to deal with that crap.
        # Yay! Except that this screws over anyone who used Ice //before// it had
        # a history, as we have no record of what they added before. Shit.
        #
        # To fix this, we provide a migration path for these people. If we have NO
        # history (not an empty history, NO history) then we fall back to our old
        # way of checking whether we manage the shortcut. The next time Ice is run
        # we will have a history to work with and can avoid using this hacky garbage.
#        if managed_ids is None:
#            return self._guess_whether_shortcut_is_managed_by_ice(shortcut, consoles)
        # We only 'manage' it if we added the shortcut in the last run
#        return shortcuts.shortcut_app_id(shortcut) in managed_ids

    def unmanaged_shortcuts(self, managed_ids, shortcuts, consoles):
        return filter(
            lambda shortcut: not self.shortcut_is_managed_by_ice(managed_ids, shortcut, consoles),
            shortcuts,
        )

    def removed_shortcuts(self, current_shortcuts, new_shortcuts):
        # To get the list of only removed shortcuts we take all of the current
        # shortcuts and filter out any that exist in the new shortcuts
        return filter(lambda shortcut: shortcut not in new_shortcuts, current_shortcuts)

    def added_shortcuts(self, current_shortcuts, new_shortcuts):
        # To get the list of only added shortcuts we take all of the new shortcuts
        # and filter out any that existed in the current shortcuts
        return filter(lambda shortcut: shortcut not in current_shortcuts, new_shortcuts)

#    def sync_roms_for_user(self, user, users_roms, consoles, dry_run=False):
    # noinspection PyStatementEffect
    def sync_roms_for_user(self, user, app_settings, dry_run=False):
        """
    This function takes care of syncing ROMs. After this function exits,
    Steam will contain only non-Ice shortcuts and the ROMs represented
    by `roms`.
    """
        # 'Unmanaged' is just the term I am using for shortcuts that the user has
        # added that Ice shouldn't delete. For example, something like a shortcut
        # to Plex would be 'Unmanaged'
#        previous_managed_ids = self.managed_rom_archive.previous_managed_ids(user)
#        logger.debug("Previous managed ids: %s" % previous_managed_ids)
#        current_shortcuts = shortcuts.get_shortcuts(user)
#        unmanaged_shortcuts = self.unmanaged_shortcuts(previous_managed_ids, current_shortcuts, consoles)
#        logger.debug("Unmanaged shortcuts: %s" % unmanaged_shortcuts)
#        current_ice_shortcuts = filter(lambda shortcut: shortcut not in unmanaged_shortcuts, current_shortcuts)
#        logger.debug("Current Ice shortcuts: %s" % current_ice_shortcuts)
        # Generate a list of shortcuts out of our list of ROMs
#        rom_shortcuts = map(roms.rom_to_shortcut, users_roms)
        # Calculate which ROMs were added and which were removed so we can inform
        # the user
#        removed = self.removed_shortcuts(current_ice_shortcuts, rom_shortcuts)
#        map(lambda shortcut: logger.info("Removing ROM: `%s`" % shortcut.name), removed)
#        added = self.added_shortcuts(current_ice_shortcuts, rom_shortcuts)
#        map(lambda shortcut: logger.info("Adding ROM: `%s`" % shortcut.name), added)

        # Set the updated shortcuts
#        updated_shortcuts = unmanaged_shortcuts + rom_shortcuts
#        logger.debug("Sync Result: %s" % updated_shortcuts)

        if dry_run:
            logger.debug("Not saving or updating history due to dry run")
            return

        ##############
        # Quick hack to try and get this thing to work

        # Open the shortcuts vdf as raw bytes and return it as bytes type and slice off the last two bytes:
        current_shortcuts = _shortcut_appender.get_shortcuts_append(user)
#        print("Current Shortcuts:", current_shortcuts)
#        print("Current Shortcuts Hex:", current_shortcuts.hex())

        #Testing if app_settings is available here:
        print(app_settings.config.game_name)

        # Set Game name from config file:
        game_name = app_settings.config.game_name
        game_name_bytes = bytes(game_name, 'utf-8')
#        print(game_name_bytes)

        # Make sure that game name doesn't already exist
        if current_shortcuts.find(game_name_bytes) != -1:
            gamealreadyexistseror = str("non-steam game " + game_name + " has already been added as a shortcut")
            raise EnvCheckerError(gamealreadyexistseror)

        # Set exe filename from config file:
#        exe = '/SuperTux.sh"'
        exe = app_settings.config.game_exe

        # Get path to exe by moving up a few directories from script location and append exe name:
        exe_path = '"' + str(Path(__file__).parents[2]) + '/' + exe + '"'
        print("exe path:", exe_path)
        exe_path_bytes = bytes(exe_path, 'utf-8')

        # Get appid
        appid = _shortcut_appender.shortcut_app_id_short(game_name, exe_path)
        appid = int(appid)
        print("appid:", appid)
        appid_bytes = appid.to_bytes(4, byteorder='little')
        print("appid in hex:", appid_bytes.hex())

        # Get start directory path via same method as above:
        start_dir = '"' + str(Path(__file__).parents[2]) + '"'
        print("start dir:", start_dir)
        start_dir_bytes = bytes(start_dir, 'utf-8')

        # Get icon path using same method as above:
        icon_path = str(Path(__file__).parents[2]) + '/Steam-Artwork/' + app_settings.config.game_icon
#        icon_path = '"' + str(Path(__file__).parents[2]) + "/Steam-Artwork/icon.ico" + '"'
        print("icon path:", icon_path)
        icon_path_bytes = bytes(icon_path, 'utf-8')

        # We are also going to need the ID for the shortcut. Find last entry, increment by 1 and convert to hex:
        entryid = _shortcut_appender.findLastEntryNumberAndPosition(current_shortcuts)
        entryid += 1
        entryid = entryid.to_bytes(1, byteorder='little')
        entryid_bytes = bytes(entryid)
        print("entryid in hex", entryid.hex())

        # This creates the new shortcuts file contents
        new_shortcut = current_shortcuts + b'\x00' + entryid_bytes + b'\x00' + b'\x02appid\x00' + appid_bytes + \
                       b'\x01AppName\x00' + game_name_bytes + b'\x00' + b'\x01Exe\x00' + exe_path_bytes + b'\x00' + \
                       b'\x01StartDir\x00' + start_dir_bytes + b'\x00' + b'\x01icon\x00' + icon_path_bytes + b'\x00' + \
                       b'\x01ShortcutPath\x00\x00' + b'\x01LaunchOptions\x00\x00' + \
                       b'\x02IsHidden\x00\x00\x00\x00\x00' + b'\x02\AllowDesktopConfig\x00\x01\x00\x00\x00' + \
                       b'\x02AllowOverlay\x00\x01\x00\x00\x00' + b'\x02OpenVR\x00' b'\x00\x00\x00\x00' + \
                       b'\x02Devkit\x00' + b'\x00\x00\x00\x00' + b'\x01DevkitGameID\x00\x00' + \
                       b'\x02DevkitOverrideAppID\x00\x00\x00\x00\x00' + b'\x02LastPlayTime\x00\x00\x00\x00\x00' + \
                       b'\x01FlatpakAppID\x00' + \
                       b'\x00\x00tags\x00' + b'\x01\x30\x00Installed locally\x00' + b'\x08\x08\x08\x08'
#        print("New Shortcut:", new_shortcut)
#        print("New Shortcut in hex:", new_shortcut.hex())

        # Overwrites the existing shortcuts.vdf with the new contents
        logger.debug("Saving shortcuts")
        _shortcut_appender.set_shortcuts(user, new_shortcut)

        # Get source and destination artwork paths for grid images:
        source_grid_path = str(Path(__file__).parents[2]) + "/Steam-Artwork/"
        dest_grid_path = paths.custom_images_directory(user)
        appid_grid = str(appid)

        # Use hardcoded values for artwork files for now just to get it working:
        source_grid_path_last = source_grid_path + app_settings.config.grid_lastplayed
        dest_grid_path_last = dest_grid_path + "/" + appid_grid + ".png"
        source_grid_path_hero = source_grid_path + app_settings.config.grid_hero
        dest_grid_path_hero = dest_grid_path + "/" + appid_grid + "_hero.png"
        source_grid_path_logo = source_grid_path + app_settings.config.grid_logo
        dest_grid_path_logo = dest_grid_path + "/" + appid_grid + "_logo.png"
        source_grid_path_p = source_grid_path + app_settings.config.grid_portrait
        dest_grid_path_p = dest_grid_path + "/" + appid_grid + "p.png"

        # copy the images
        shutil.copy(source_grid_path_last, dest_grid_path_last)
        shutil.copy(source_grid_path_hero, dest_grid_path_hero)
        shutil.copy(source_grid_path_logo, dest_grid_path_logo)
        shutil.copy(source_grid_path_p, dest_grid_path_p)

        print("Shortcut Has Been Created!!")
