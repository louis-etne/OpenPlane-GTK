#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane import config
from openplane.gui.logbook.flight_view import *


class Logbook:

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file('openplane/gui/logbook/logbook.glade')

        self.window = builder.get_object('mainWindow')
        # On défini l'icône de la fenêtre
        self.window.set_icon_from_file(config.icon_path)
        # On affiche la fenêtre en plein écran
        self.window.maximize()

        # On récupère la grille où l'on va attacher les différents widgets
        grid = builder.get_object('layout')

        # On créer la vue des vols
        self.flight_view = FlightView()
        # Et on l'importe directement dans la grille
        grid.attach(self.flight_view, 1, 0, 1, 1)
