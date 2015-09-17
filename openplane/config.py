#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

import os

# Folders
gui_folder = 'openplane{0}gui{0}'.format(os.sep)
glade_folder = 'openplane{0}gui{0}glade{0}'.format(os.sep)
images_folder = 'openplane{0}images{0}'.format(os.sep)
planes_folder = 'openplane{0}planes{0}'.format(os.sep)
flightslog_folder = 'openplane{0}flightslog{0}'.format(os.sep)

# Logo (Thanks to Blackline)
logo_file_name = 'OpenPlane.png'
icon32_file_name = 'OpenPlane_32.png'
icon64_file_name = 'OpenPlane_64.png'
logo_path = '{}{}'.format(images_folder, logo_file_name)
icon32_path = '{}{}'.format(images_folder, icon32_file_name)
icon64_path = '{}{}'.format(images_folder, icon64_file_name)

# Glade files
hangar = '{}gui_hangar.glade'.format(glade_folder)
plane_manager = '{}gui_plane_manager.glade'.format(glade_folder)
weight = '{}gui_weight.glade'.format(glade_folder)
app = '{}gui_app.glade'.format(glade_folder)
about = '{}gui_about.glade'.format(glade_folder)
convert = '{}gui_convert.glade'.format(glade_folder)
flights_log = '{}gui_flightslog.glade'.format(glade_folder)

# Images
preview_balance = '{}preview_balance.png'.format(images_folder)
preview = '{}preview.png'.format(images_folder)

# Extensions
planes_ext = '.opp'
flights_ext = '.opf'
