#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk


class HelpWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Aide')

        self.set_border_width(10)
        self.set_resizable(False)

        main_layout = Gtk.Grid()
        main_layout.set_row_spacing(10)
        main_layout.set_column_spacing(6)
        main_layout.set_row_homogeneous(False)
        main_layout.set_column_homogeneous(True)
        self.add(main_layout)

        logo = Gtk.Image.new_from_file('logo.png')
        main_layout.attach(logo, 0, 0, 2, 1)

        app_label = Gtk.Label()
        app_label.set_markup('<b>LibreAero</b>')
        main_layout.attach(app_label, 0, 1, 2, 1)

        version_label = Gtk.Label()
        version_label.set_markup('0.3.0:Alpha')
        main_layout.attach(version_label, 0, 2, 2, 1)

        description_label = Gtk.Label()
        description_label.set_markup('Une petite description de l\'application')
        main_layout.attach(description_label, 0, 3, 2, 1)

        web_label = Gtk.Label()
        web_label.set_markup('<a href="http://test.com/">Website</a>')
        main_layout.attach(web_label, 0, 4, 2, 1)

        copyright_label = Gtk.Label()
        copyright_label.set_markup('<small>Copyright © 2015 Louis Etienne</small>')
        main_layout.attach(copyright_label, 0, 5, 2, 1)

        btn_quit = Gtk.Button(label='Fermer')
        btn_quit.connect('clicked', self.app_quit)
        main_layout.attach(btn_quit, 1, 6, 1, 1)

    def app_quit(self, *args):
        self.destroy()

if __name__ == '__main__':
    win = HelpWindow()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
