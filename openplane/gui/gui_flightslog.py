#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane import config
from openplane.core.Flight import *
from openplane.core.Plane import *
from openplane.gui.gui_flight_manager import *
import glob
import os


class FlightsLogWindow:

    def __init__(self, flight_path=None):
        builder = Gtk.Builder()
        builder.add_from_file(config.flights_log)

        # Les signaux
        handlers = {
            'on_close_clicked': self.app_quit,
            'on_add_clicked': self.on_add_clicked,
            'on_flight_selected': self.on_flight_selected
        }

        builder.connect_signals(handlers)

        self.flights_list = builder.get_object('flight_store')
        self.update_flights_list()
        selector = builder.get_object('flightsLogSelect')

        # Btns
        self.btn_open = builder.get_object('open')
        self.btn_open.connect('clicked', self.on_open_clicked, selector)
        self.btn_delete = builder.get_object('delete')
        self.btn_delete.connect('clicked', self.on_delete_clicked, selector)

        # Fenêtre principale
        self.view = builder.get_object('flightsLogView')
        self.view.set_rules_hint(True)
        self.window = builder.get_object('mainWindow')
        self.window.set_icon_from_file(config.icon_path)

        if flight_path is not None:
            self.import_flightlog(flight_path)

    def update_flights_list(self):
        '''
            Met à jour la liste des avions par rapport aux fichiers contenu
            dans le dossier flightslog
        '''
        self.flights_list.clear()
        flights_path = []

        for flight_file in glob.glob('{}*{}'.format(config.flightslog_folder,
                                                    config.flights_ext)):
            flights_path.append(flight_file)

        for flight_doc in flights_path:
            flight = Flight()
            plane = Plane()

            flight.import_flight(flight_doc)

            total_hours = flight.calc_total_hours()

            # On vérifie que l'avion existe bien (bug remonté par WinXaito)
            if os.path.isfile(flight.plane):
                plane.import_plane(flight.plane)
                self.flights_list.append([flight.date, plane.matriculation,
                                         flight.type, total_hours])
            else:
                self.flights_list.append([flight.date, 'UKNOWN',
                                         flight.type, total_hours])

    def on_flight_selected(self, select):
        '''
            Change l'état des boutons quand un vol est sélectionné
        '''
        model, treeiter = select.get_selected()
        if treeiter is not None:
            if not self.btn_open.get_sensitive():
                self.btn_open.set_sensitive(True)

            if not self.btn_delete.get_sensitive():
                self.btn_delete.set_sensitive(True)
        else:
            self.btn_open.set_sensitive(False)
            self.btn_delete.set_sensitive(False)

    def on_add_clicked(self, button):
        '''
            Ouvre l'éditeur de vol afin de créer un nouveau vol
        '''
        flight_manager = FlightManagerDialog()
        flight_manager.dialog.run()
        self.update_flights_list()

    def on_open_clicked(self, button, selection):
        '''
            Ouvre l'éditeur de vol en passant le lien du vol à éditer
        '''
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            file_name = model[treeiter][0]
            path = '{}{}{}'.format(config.flightslog_folder, file_name,
                                   config.flights_ext)

            flight_manager = FlightManagerDialog(path)
            flight_manager.dialog.run()

            self.update_flights_list()

    def on_delete_clicked(self, button, selection):
        '''
            Supprime le fichier correspondant au vol sélectionné
        '''
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            file_name = model[treeiter][0]
            os.remove('{}{}{}'.format(config.flightslog_folder, file_name,
                                      config.flights_ext))
            self.update_flights_list()

    def import_flightlog(self, flight_path):
        flight = Flight()
        flight.import_flight(flight_path)

    def app_quit(self, *args):
        '''
            Supprime la fenêtre
        '''
        self.window.destroy()
