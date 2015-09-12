#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from openplane.gui.gui_app import *

win = App()
win.connect('delete-event', win.app_quit)
win.show_all()
Gtk.main()
