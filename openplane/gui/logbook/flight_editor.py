#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk, GdkPixbuf
import os

from openplane import config
from openplane.gui.gui_airfields_selector import *
from openplane.gui.gui_hangar import *
from openplane.core.Flight import *
from openplane.core.Plane import *


class FlightEditor(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self)

        builder = Gtk.Builder()
        builder.add_from_file('openplane/gui/logbook/flight_editor.glade')

        # On récupère le layout principal qu'on attache ensuite à cette classe
        main_layout = builder.get_object('FlightEditor')
        self.pack_start(main_layout, True, True, 0)

        # On récupère tous les widgets de la fenêtre
        self.get_widgets(builder)
        # Et on les figes
        self.set_widgets_sensitive(False)

        # On charge la liste des types de vol
        self.load_flight_type_values(builder)

        # Pour finir, on définit tous les handlers
        handlers = {
            'on_add_plane': self.select_plane,
            'on_add_airfield': self.select_airfield
        }
        # Et on les connecte grâce au builder
        builder.connect_signals(handlers)


    def get_widgets(self, builder):
        '''
        Récupère tous les widgets
        '''
        self.save = builder.get_object('save')
        self.cancel = builder.get_object('cancel')

        self.type = builder.get_object('flightType')
        self.id = builder.get_object('id')

        self.calendar = builder.get_object('calendar')

        self.add_plane_btn = builder.get_object('selectPlane')
        self.flight_rule = builder.get_object('flightRules')

        self.from_btn = builder.get_object('selectFrom')
        self.departure_hours = builder.get_object('inHours')
        self.departure_minutes = builder.get_object('inMinutes')

        self.to_btn = builder.get_object('selectTo')
        self.arrival_hours = builder.get_object('outHours')
        self.arrival_minutes = builder.get_object('outMinutes')

        self.day_hours = builder.get_object('dayFlightHours')
        self.day_minutes = builder.get_object('dayFlightMinutes')

        self.night_hours = builder.get_object('nightFlightHours')
        self.night_minutes = builder.get_object('nightFlightMinutes')

        self.takeoffs_nb = builder.get_object('takeoffsNb')
        self.landings_nb = builder.get_object('landingsNb')

        self.crew_view = builder.get_object('crewView')
        self.add_crew_btn = builder.get_object('addCrew')
        self.crew_list = builder.get_object('crewList')

        self.briefing = builder.get_object('note')
        self.briefing_buffer = builder.get_object('briefingBuffer')


    def load_flight_type_values(self, builder):
        '''
        Met en place la ComboBox (image + nom + id)
        À lancer à l'initialisation de l'éditeur de vol
        '''
        # On récupère la liste des types de vol
        type_list = builder.get_object('typeFlight')

        # On crée la liste
        # L'item avion
        type_list.append([GdkPixbuf.Pixbuf.new_from_file(config.plane),
                          'Avion',
                          'plane'])
        # L'item du simulateur
        type_list.append([GdkPixbuf.Pixbuf.new_from_file(config.simulator),
                          'Simulateur',
                          'simulator'])

        self.type.set_active(0)


    def set_widgets_sensitive(self, sensitive):
        '''
        Défini si l'utilisateur peut intéragir avec les widgets
        '''
        self.type.set_sensitive(sensitive)
        self.id.set_sensitive(sensitive)

        self.calendar.set_sensitive(sensitive)

        self.add_plane_btn.set_sensitive(sensitive)
        self.flight_rule.set_sensitive(sensitive)

        self.from_btn.set_sensitive(sensitive)
        self.departure_hours.set_sensitive(sensitive)
        self.departure_minutes.set_sensitive(sensitive)

        self.to_btn.set_sensitive(sensitive)
        self.arrival_hours.set_sensitive(sensitive)
        self.arrival_minutes.set_sensitive(sensitive)

        self.day_hours.set_sensitive(sensitive)
        self.day_minutes.set_sensitive(sensitive)

        self.night_hours.set_sensitive(sensitive)
        self.night_minutes.set_sensitive(sensitive)

        self.takeoffs_nb.set_sensitive(sensitive)
        self.landings_nb.set_sensitive(sensitive)

        self.crew_view.set_sensitive(sensitive)
        self.add_crew_btn.set_sensitive(sensitive)

        self.briefing.set_sensitive(sensitive)


    def import_flight(self, path):
        '''
        Importe les valeurs du fichier au chemin spécifié dans
        l'éditeur de vol
        '''
        # On vérifie qu'on ai bien le chemin
        if path is not None:
            # On crée le vol
            flight = Flight()
            flight.import_flight(path)

            # On règle les différents widgets
            # Ignoré si flight.type est inconnu
            self.type.set_active_id(flight.type)
            self.id.set_text(flight.id)
            self.set_date(flight)

            self.set_plane(flight)
            self.flight_rule.set_active_id(flight.flight_rule)

            self.from_btn.set_label(flight.departure_airfield)
            self.departure_hours.set_value(flight.departure_hours)
            self.departure_minutes.set_value(flight.departure_minutes)

            self.to_btn.set_label(flight.departure_airfield)
            self.arrival_hours.set_value(flight.arrival_hours)
            self.arrival_minutes.set_value(flight.arrival_minutes)

            self.day_hours.set_value(flight.time_day_hours)
            self.day_minutes.set_value(flight.time_day_minutes)

            self.night_hours.set_value(flight.time_night_hours)
            self.night_minutes.set_value(flight.time_night_minutes)

            self.takeoffs_nb.set_value(flight.takeoffs)
            self.landings_nb.set_value(flight.landings)

            self.set_crew(flight)

            self.briefing_buffer.set_text(flight.briefing)


    def set_date(self, flight):
        '''
        Règle le calendrier sur la date entrée (flight.date)
        En oubliant pas que dans Gtk, n° du mois = n°-1

        - Exemple :
            Juin est le 6ème mois, il sera donc le 5ème pour Gtk
        '''
        # On récupère le jour, le mois et l'année
        day = flight.return_day()
        # On décale l'indice
        month = flight.return_month() - 1
        year = flight.return_year()

        # On règle le calendrier
        self.calendar.select_day(day)
        self.calendar.select_month(month, year)


    def set_plane(self, flight):
        '''
        Met le label du bouton de sélection d'avion sur le nom
        de l'avion si existant, sur UNKNOWN si non
        '''
        # On regarde si le fichier existe bien
        if os.path.isfile(flight.plane):
            # On en crée un avion
            plane = Plane()
            plane.import_plane(flight.plane)

            self.add_plane_btn.set_label(plane.matriculation)
        else:
            self.add_plane_btn.set_label('UNKNOWN')


    def set_crew(self, flight):
        '''
        Importe les membres d'équipage dans l'éditeur de vol
        '''
        # Rien ne sert de nettoyer la liste si il n'y a pas d'équipage
        if len(flight.crew) > 0:
            self.crew_list.clear()

            for person in flight.crew:
                # Valeurs possibles :
                # Pilot, Captain, Co-pilot, Passenger et Instructor
                if person[1] == 'Captain':
                    role = 'Commandant de bord'
                elif person[1] == 'Co-pilot':
                    role = 'Co-pilote'
                elif person[1] == 'Passenger':
                    role = 'Passager'
                elif person[1] == 'Instructor':
                    role = 'Instructeur'
                else:
                    role = 'Pilote'

                self.crew_list.append([person[0], role])


    def select_plane(self, button):
        '''
        Ouvre le hangar afin de sélectionner un avion
        '''
        selector = HangarDialog(True)
        response = selector.dialog.run()

        # Le bouton valider renvoie 1
        if response == 1:
            button.set_label(selector.return_selected())

        selector.dialog.destroy()


    def select_airfield(self, button):
        '''
        Ouvre le sélecteur de terrain et met le label du boutton sur le
        terrain sélectionné.
        '''
        selector = AirfieldSelectorDialog()
        response = selector.dialog.run()

        if response == 1:
            button.set_label(selector.return_airfield())

        selector.dialog.destroy()