#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk, GdkPixbuf
from openplane import config
from openplane import text


class AboutDialog:

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file(config.about)

        handler = {'on_quit_clicked': self.app_quit}
        builder.connect_signals(handler)

        self.dialog = builder.get_object('aboutDialog')
        self.dialog.set_version(text.version)

        logo = GdkPixbuf.Pixbuf.new_from_file(config.icon64_path)
        self.dialog.set_logo(logo)

        self.dialog.set_icon_from_file(config.icon_path)

    def app_quit(self, *btn):
        self.dialog.destroy()
