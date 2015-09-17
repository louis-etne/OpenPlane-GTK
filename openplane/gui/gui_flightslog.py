#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane import config


class FlightsLogWindow:

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file(config.flights_log)

        self.window = builder.get_object('mainWindow')

    def app_quit(self, *args):
        self.window.destroy()
