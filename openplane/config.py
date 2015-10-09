#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

import os

# Folders
gui_folder = 'openplane{0}gui{0}'.format(os.sep)
glade_folder = 'openplane{0}gui{0}glade{0}'.format(os.sep)
images_folder = 'openplane{0}images{0}'.format(os.sep)
planes_folder = 'openplane{0}datas{0}planes{0}'.format(os.sep)
logbook_folder = 'openplane{0}datas{0}logbook{0}'.format(os.sep)

# Files
airfields = 'openplane{0}datas{0}airfields.json'.format(os.sep)

# Logo (Thanks to Blackline)
logo_file_name = 'OpenPlane.png'
icon32_file_name = 'OpenPlane_32.png'
icon64_file_name = 'OpenPlane_64.png'
logo_path = '{}{}'.format(images_folder, logo_file_name)

if os.name == 'posix':
    icon_path = '{}{}'.format(images_folder, icon64_file_name)
else:
    icon_path = '{}{}'.format(images_folder, icon32_file_name)

# Glade files
app = '{}app.glade'.format(glade_folder)
about = '{}about.glade'.format(glade_folder)
hangar = '{}hangar.glade'.format(glade_folder)
weight = '{}weight.glade'.format(glade_folder)
convert = '{}convert.glade'.format(glade_folder)
crew_adder = '{}crew_adder.glade'.format(glade_folder)
plane_manager = '{}plane_manager.glade'.format(glade_folder)
update_manager = '{}update_manager.glade'.format(glade_folder)
airfield_viewer = '{}airfield_viewer.glade'.format(glade_folder)
airfields_selector = '{}airfields_selector.glade'.format(glade_folder)

logbook = '{}logbook{}{}'.format(gui_folder, os.sep, 'logbook.glade')
flight_view = '{}logbook{}{}'.format(gui_folder, os.sep, 'flight_view.glade')
flight_editor = '{}logbook{}{}'.format(gui_folder, os.sep, 'flight_editor.glade')

# Images
preview_balance = '{}preview_balance.png'.format(images_folder)
preview = '{}preview.png'.format(images_folder)
plane = '{}plane.png'.format(images_folder)
simulator = '{}joystick.png'.format(images_folder)
model = '{}model.png'.format(images_folder)

# Extensions
planes_ext = '.opp'
flights_ext = '.opf'
