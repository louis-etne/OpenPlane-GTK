#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk, GdkPixbuf
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

        # On charge les listes des type de vol
        self.set_type_list()

        # On appelle les handlers & on les connecte
        handlers = {'on_toggled': self.filter_chose}
        builder.connect_signals(handlers)


    def get_buttons(self, builder):
        '''
        Récupère les boutons utilent de l'interface
        '''
        self.last7days = builder.get_object('7LastDays')
        self.last28days = builder.get_object('28LastDays')
        self.last6months = builder.get_object('6LastMonths')
        self.last12months = builder.get_object('12LastMonths')

        self.day = builder.get_object('allDayEntries')
        self.night = builder.get_object('allNightEntries')

        self.vfr = builder.get_object('allVfrEntries')
        self.ifr = builder.get_object('allIfrEntries')

        self.type = builder.get_object('type')
        self.type_list = builder.get_object('typeStore')


    def set_type_list(self):
        '''
        Définit les options pour la liste des types de vol
        '''
        self.type_list.append([None, 'Tous', 'all'])

        # L'item avion
        self.type_list.append([GdkPixbuf.Pixbuf.new_from_file(config.plane),
                               'Avion', 'plane'])
        # L'item du simulateur
        self.type_list.append([GdkPixbuf.Pixbuf.new_from_file(config.simulator),
                               'Simulateur', 'simulator'])
        # L'item modelisme
        self.type_list.append([GdkPixbuf.Pixbuf.new_from_file(config.model),
                               'Modélisme', 'model'])

        self.type.set_active(0)


    def filter_chose(self, button):
        f_type = 'all'
        date = 'all'
        rule = 'all'
        day = 'all'

        if self.last7days.get_active():
            date = 'week'
        elif self.last28days.get_active():
            date = 'month'
        elif self.last6months.get_active():
            date = '6months'
        elif self.last12months.get_active():
            date = 'year'
        else:
            date = 'all'

        if self.day.get_active():
            day = 'day'
        elif self.night.get_active():
            day = 'night'
        else:
            day = 'all'

        if self.vfr.get_active():
            rule = 'vfr'
        elif self.ifr.get_active():
            rule = 'ifr'
        else:
            rule = 'all'

        f_type = self.type.get_active_id()

        self.flight_view.reload_flight(date, day, rule, f_type)