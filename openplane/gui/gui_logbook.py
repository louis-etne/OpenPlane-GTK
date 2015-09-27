#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane.core.Flight import *
from openplane import config


class LogbookWindow:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file(config.logbook)

        handlers = {'on_close': self.app_quit}
        builder.connect_signals(handlers)

        self.window = builder.get_object('mainWindow')
        self.window.set_icon_from_file(config.icon_path)
        self.window.maximize()

    def app_quit(self, widget):
        self.window.destroy()
