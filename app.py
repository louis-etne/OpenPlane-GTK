#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from openplane.gui.gui_app import *

app = App()
app.connect('delete-event', app.app_quit)
app.show_all()
Gtk.main()
