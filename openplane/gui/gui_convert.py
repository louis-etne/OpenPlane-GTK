#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane.gui.gui_help import *
from openplane.core.convert import *


class ConvertWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='Convertisseur')
        self.set_border_width(10)
        self.set_resizable(False)
        self.create_gui()
        self.on_units_changed()

    def create_gui(self):
        '''
            Met en place l'interface graphique
        '''

        # Le layout principal
        main_layout = Gtk.Grid()
        main_layout.set_row_spacing(6)
        main_layout.set_column_spacing(6)
        main_layout.set_row_homogeneous(False)
        main_layout.set_column_homogeneous(False)

        # L'entrée
        adjustment = Gtk.Adjustment(0, -5000, 300000, 1, 10, 0)
        self.entry = Gtk.SpinButton()
        self.entry.set_adjustment(adjustment)
        self.entry.set_value(0)  # On met 0 comme valeur par défaut
        self.entry.connect('value-changed', self.on_units_changed)
        main_layout.attach(self.entry, 0, 0, 1, 1)

        # Les différentres unitées
        units = Gtk.ListStore(str, str)
        units.append(['m', 'Mètre(s)'])
        units.append(['km', 'Kilomètre(s)'])
        units.append(['ft', 'Pied(s)'])
        units.append(['nm', 'Mile(s) Nautique'])
        units.append(['c', 'Degré(s) Celsius'])
        units.append(['f', 'Degré(s) Fahrenheit'])
        units.append(['k', 'Kelvin'])

        # On met en place la liste
        self.units_combo = Gtk.ComboBox.new_with_model_and_entry(units)
        self.units_combo.set_entry_text_column(1)
        self.units_combo.set_active(0)  # On définit 'mètre' par défaut
        self.units_combo.connect('changed', self.on_units_changed)
        main_layout.attach(self.units_combo, 1, 0, 1, 1)

        self.convert_label = Gtk.Label()
        self.convert_label.set_justify(Gtk.Justification.CENTER)
        self.convert_label.set_selectable(True)
        main_layout.attach(self.convert_label, 0, 1, 2, 1)

        btn_layout = Gtk.Box(spacing=6)

        btn_help = Gtk.Button(label='Aide')
        btn_help.connect('clicked', self.on_help_pressed)
        btn_layout.pack_start(btn_help, True, True, 0)

        btn_quit = Gtk.Button(label='Fermer')
        btn_quit.connect('clicked', self.app_quit)
        btn_layout.pack_start(btn_quit, True, True, 0)

        main_layout.attach(btn_layout, 1, 2, 1, 1)

        self.add(main_layout)

    def on_units_changed(self, combo=None):
        tree_iter = self.units_combo.get_active_iter()
        if tree_iter is not None:
            model = self.units_combo.get_model()
            row_id, name = model[tree_iter][:2]

            value = self.entry.get_value()
            result = None

            if row_id == 'm':
                result = 'Kilomètre(s) : {}km\n'.format(meters2kilometers(value))
                result += 'Pied(s) : {}ft\n'.format(meters2feet(value))
                result += 'Mile(s) Nautique : {}NM'.format(meters2miles(value))

            elif row_id == 'km':
                result = 'Mètre(s) : {}m\n'.format(kilometers2meters(value))
                result += 'Pied(s) : {}ft\n'.format(kilometers2feet(value))
                result += 'Mile(s) Nautique : {}NM'.format(kilometers2miles(value))

            elif row_id == 'ft':
                result = 'Mètre(s) : {}m\n'.format(feet2meters(value))
                result += 'Kilomètre(s) : {}km\n'.format(feet2kilometers(value))
                result += 'Mile(s) Nautique : {}NM'.format(feet2miles(value))

            elif row_id == 'nm':
                result = 'Mètre(s) : {}m\n'.format(miles2meters(value))
                result += 'Kilomètre(s) : {}km\n'.format(miles2kilometers(value))
                result += 'Pied(s) : {}ft'.format(miles2feet(value))

            elif row_id == 'c':
                result = 'Degré(s) Fahrenheit : {}°F\n'.format(celsius2fahrenheit(value))
                result += 'Kelvin : {}K\n'.format(celsius2kelvin(value))

            elif row_id == 'f':
                result = 'Degré(s) Celsius : {}°C\n'.format(fahrenheit2celsius(value))
                result += 'Kelvin : {}K\n'.format(fahrenheit2kelvin(value))

            elif row_id == 'k':
                result = 'Degré(s) Celsius : {}°C\n'.format(kelvin2celsius(value))
                result += 'Degré(s) Fahrenheit : {}°F\n'.format(kelvin2fahrenheit(value))

            self.convert_label.set_text(result)
        else:
            pass

    def on_help_pressed(self, *args):
        help_window = HelpWindow()
        help_window.connect('delete-event', help_window.app_quit)
        help_window.show_all()

    def app_quit(self, *args):
        self.destroy()

if __name__ == '__main__':
    win = ConvertWindow()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
