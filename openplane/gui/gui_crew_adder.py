#!/usr/bin/env python
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane import config

class CrewAdderDialog:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(config.crew_adder)

        handler = {'on_cancel': self.app_quit}
        self.builder.connect_signals(handler)

        self.dialog = self.builder.get_object('dialog')
        self.dialog.set_icon_from_file(config.icon_path)

    def return_value(self):
        name = self.builder.get_object('name')
        role = self.builder.get_object('role')

        return [name.get_text(), role.get_active_id()]

    def app_quit(self, button=None):
        self.dialog.destroy()
