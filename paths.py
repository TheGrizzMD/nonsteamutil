# encoding: utf-8

import os


def application_data_directory():
    # I changed this from Ice, this should now just be the path of where the nonsteamutil script is
    return os.path.dirname(os.path.realpath(__file__))


def data_file_path(filename):
    return os.path.join(application_data_directory(), filename)


def archive_path():
    return data_file_path('archive.json')


def log_file_location():
    return data_file_path('nonsteamutil.log')


def default_roms_directory():
    return os.path.join(os.path.expanduser('~'), 'ROMs')
