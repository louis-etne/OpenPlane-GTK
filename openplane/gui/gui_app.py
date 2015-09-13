#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane.gui.gui_convert import *
from openplane.gui.gui_hangar import *
from openplane.gui.gui_weight import *
from openplane.gui.gui_help import *


class App(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='OpenPlane')

        self.set_border_width(10)

        main_layout = Gtk.Grid()
        main_layout.set_row_spacing(6)
        main_layout.set_column_spacing(6)
        main_layout.set_row_homogeneous(True)
        main_layout.set_column_homogeneous(True)

        # Convertisseur
        btn_convert = Gtk.Button(label='Convertisseur')
        btn_convert.connect('clicked', self.on_convert_pressed)
        main_layout.attach(btn_convert, 0, 0, 3, 1)

        # Hangar
        btn_hangar = Gtk.Button(label='Accéder au hangar')
        btn_hangar.connect('clicked', self.on_hangar_pressed)
        main_layout.attach(btn_hangar, 0, 1, 3, 1)

        # Masse et centrage
        btn_weight = Gtk.Button(label='Masse et centrage')
        btn_weight.connect('clicked', self.on_weight_pressed)
        main_layout.attach(btn_weight, 0, 2, 3, 1)

        btn_help = Gtk.Button(label='Aide')
        btn_help.connect('clicked', self.on_help_pressed)
        main_layout.attach(btn_help, 1, 3, 1, 1)

        btn_quit = Gtk.Button(label='Quitter')
        btn_quit.connect('clicked', self.app_quit)
        main_layout.attach(btn_quit, 2, 3, 1, 1)

        self.add(main_layout)

    def on_convert_pressed(self, *args):
        convert = ConvertWindow()
        convert.connect('delete-event', convert.app_quit)
        convert.show_all()

    def on_hangar_pressed(self, *args):
        hangar = HangarDialog()
        hangar.dialog.run()

    def on_weight_pressed(self, *args):
        weight = WeightWindow()
        weight.window.connect('delete-event', weight.app_quit)
        weight.window.show_all()

    def on_help_pressed(self, *args):
        help_window = HelpWindow()
        help_window.connect('delete-event', help_window.app_quit)
        help_window.show_all()

    def app_quit(self, *args):
        Gtk.main_quit()

if __name__ == '__main__':
    win = App()
    win.connect('delete-event', win.app_quit)
    win.show_all()
    Gtk.main()
