# encoding: utf-8

import collections

AppSettings = collections.namedtuple('AppSettings', [
  'config',
#  'consoles',
#  'emulators',
])

Configuration = collections.namedtuple('Configuration', [
  'backup_directory',
  'provider_spec',
  'roms_directory',
  'userdata_directory',
  'game_name',
  'game_exe',
  'game_icon',
  'grid_lastplayed',
  'grid_hero',
  'grid_logo',
  'grid_portrait',
])

Console = collections.namedtuple('Console', [
  'fullname',
  'shortname',
  'extensions',
  'custom_roms_directory',
  'prefix',
  'icon',
  'images_directory',
  'emulator',
])

Emulator = collections.namedtuple('Emulator', [
  'name',
  'location',
  'format',
])

ROM = collections.namedtuple('ROM', [
  'name',
  'path',
  'console',
])