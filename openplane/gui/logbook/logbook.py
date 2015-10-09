#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane import config
from openplane.gui.logbook.flight_view import *


class Logbook:

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file(config.logbook)

        self.window = builder.get_object('mainWindow')
        # On défini l'icône de la fenêtre
        self.window.set_icon_from_file(config.icon_path)
        # On affiche la fenêtre en plein écran
        self.window.maximize()

        # On récupère la grille où l'on va attacher les différents widgets
        grid = builder.get_object('layout')

        # On créer la vue des vols
        self.flight_view = FlightView(self)
        # Et on l'importe directement dans la grille
        grid.attach(self.flight_view, 1, 0, 1, 1)

        # On récupère tous les boutons
        self.get_buttons(builder)


    def get_buttons(self, builder):
        '''
        Récupère tous les boutons de l'interface
        '''
        self.all_entries = builder.get_object('allEntries')
        self.last7days = builder.get_object('7LastDays')
        self.last28days = builder.get_object('28LastDays')
        self.last6months = builder.get_object('6LastMonths')
        self.last12months = builder.get_object('12LastMonths')


    def unselect_buttons(self):
        '''
        Désactive les boutons
        '''
        self.all_entries.set_active(False)
        self.last7days.set_active(False)
        self.last28days.set_active(False)
        self.last6months.set_active(False)
        self.last12months.set_active(False)