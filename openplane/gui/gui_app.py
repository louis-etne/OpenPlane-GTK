#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane.gui.gui_convert import *
from openplane.gui.gui_hangar import *
from openplane.gui.gui_weight import *
from openplane.gui.gui_about import *
from openplane import config


class App:
    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file(config.app)

        handlers = {
            'on_mainWindow_delete_event': self.app_quit,
            'on_quit_clicked': self.app_quit,
            'on_convert_clicked': self.on_convert_clicked,
            'on_hangar_clicked': self.on_hangar_clicked,
            'on_weight_clicked': self.on_weight_clicked,
            'on_about_clicked': self.on_about_clicked
        }

        builder.connect_signals(handlers)
        self.window = builder.get_object('mainWindow')
        self.window.set_icon_from_file(config.icon_path)

    def on_convert_clicked(self, *args):
        convert = ConvertWindow()
        convert.window.show_all()

    def on_hangar_clicked(self, *args):
        hangar = HangarDialog()
        hangar.dialog.run()

    def on_weight_clicked(self, *args):
        weight = WeightWindow()
        weight.window.show_all()

    def on_about_clicked(self, *args):
        about = AboutDialog()
        about.dialog.run()
        about.dialog.destroy()

    def app_quit(self, *args):
        Gtk.main_quit()
