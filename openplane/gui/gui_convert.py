#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane.gui.gui_about import *
from openplane.core.convert import *
from openplane import text
from openplane import config


class ConvertWindow:

    def __init__(self):
        self.create_gui()
        self.on_units_changed()

    def create_gui(self):
        '''
            Met en place l'interface graphique
        '''

        builder = Gtk.Builder()
        builder.add_from_file(config.convert)
        main_layout = builder.get_object('mainLayout')

        # L'entrée
        adjustment = Gtk.Adjustment(0, -5000, 300000, 1, 10, 0)
        self.entry = Gtk.SpinButton()
        self.entry.set_adjustment(adjustment)
        self.entry.set_value(0)  # On met 0 comme valeur par défaut
        self.entry.connect('value-changed', self.on_units_changed)
        main_layout.attach(self.entry, 0, 0, 1, 1)

        # Les différentres unitées
        units = Gtk.ListStore(str, str)
        units.append(['m', text.meters])
        units.append(['km', text.kilometers])
        units.append(['ft', text.feet])
        units.append(['nm', text.nm])
        units.append(['c', text.celsius])
        units.append(['f', text.fahrenheit])
        units.append(['k', text.kelvin])

        # On met en place la liste
        self.units_combo = Gtk.ComboBox.new_with_model(units)
        renderer_text = Gtk.CellRendererText()
        self.units_combo.pack_start(renderer_text, True)
        self.units_combo.add_attribute(renderer_text, "text", 1)
        self.units_combo.set_active(0)  # On définit 'mètre' par défaut
        self.units_combo.connect('changed', self.on_units_changed)
        main_layout.attach(self.units_combo, 1, 0, 1, 1)

        self.convert_label = Gtk.Label()
        self.convert_label.set_justify(Gtk.Justification.CENTER)
        self.convert_label.set_selectable(True)
        main_layout.attach(self.convert_label, 0, 1, 2, 1)

        handlers = {
            'on_delete_event': self.app_quit,
            'on_about_clicked': self.on_about_clicked,
            'on_close_clicked': self.app_quit
        }

        builder.connect_signals(handlers)

        self.window = builder.get_object('mainWindow')

    def on_units_changed(self, combo=None):
        tree_iter = self.units_combo.get_active_iter()
        if tree_iter is not None:
            model = self.units_combo.get_model()
            row_id, name = model[tree_iter][:2]

            value = self.entry.get_value()
            result = None

            if row_id == 'm':
                result = '{0} : {1}km\n'.format(text.kilometers,
                                                meters2kilometers(value))
                result += '{0} : {1}ft\n'.format(text.feet, meters2feet(value))
                result += '{0} : {1}NM'.format(text.nm, meters2miles(value))

            elif row_id == 'km':
                result = '{0} : {1}m\n'.format(text.meters,
                                               kilometers2meters(value))
                result += '{0} : {1}ft\n'.format(text.feet,
                                                 kilometers2feet(value))
                result += '{0} : {1}NM'.format(text.nm,
                                               kilometers2miles(value))

            elif row_id == 'ft':
                result = '{0} : {1}m\n'.format(text.meters, feet2meters(value))
                result += '{0} : {1}km\n'.format(text.kilometers,
                                                 feet2kilometers(value))
                result += '{0} : {1}NM'.format(text.nm, feet2miles(value))

            elif row_id == 'nm':
                result = '{0} : {1}m\n'.format(text.meters,
                                               miles2meters(value))
                result += '{0} : {1}km\n'.format(text.kilometers,
                                                 miles2kilometers(value))
                result += '{0} : {1}ft'.format(text.feet, miles2feet(value))

            elif row_id == 'c':
                result = '{0} : {1}°F\n'.format(text.fahrenheit,
                                                celsius2fahrenheit(value))
                result += '{0} : {1}K\n'.format(text.kelvin,
                                                celsius2kelvin(value))

            elif row_id == 'f':
                result = '{0} : {1}°C\n'.format(text.celsius,
                                                fahrenheit2celsius(value))
                result += '{0} : {1}K\n'.format(text.kelvin,
                                                fahrenheit2kelvin(value))

            elif row_id == 'k':
                result = '{0} : {1}°C\n'.format(text.celsius,
                                                kelvin2celsius(value))
                result += '{0} : {1}°F\n'.format(text.fahrenheit,
                                                 kelvin2fahrenheit(value))

            self.convert_label.set_text(result)
        else:
            pass

    def on_about_clicked(self, *args):
        about = AboutDialog()
        about.dialog.run()
        about.dialog.destroy()

    def app_quit(self, *args):
        self.window.destroy()
