#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne


import openplane.core.update_airfields as update_airfields
from gi.repository import Gtk
from openplane import config
from openplane import text


class UpdateManager:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file(config.update_manager)

        handlers = {
            'on_close': self.app_quit,
            'on_update_airfields_clicked': self.update_airfields
        }
        builder.connect_signals(handlers)

        self.dialog = builder.get_object('dialog')

    def update_airfields(self, btn):
        update_airfields.main()
        btn.set_label(text.to_date)
        btn.set_sensitive(False)

    def app_quit(self, widget):
        self.dialog.destroy()
