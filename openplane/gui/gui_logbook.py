#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk, GdkPixbuf
from openplane.core.Flight import *
from openplane.gui.gui_airfields_selector import *
from openplane.gui.gui_hangar import *
from openplane import config
import os


class LogbookWindow:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(config.logbook)

        handlers = {
            'on_close': self.app_quit,
            'on_add_flight': self.add_flight,
            'on_select_plane': self.select_plane,
            'on_select_airfield': self.select_airfield,
            'on_add_crew': self.add_crew,
            'on_cursor_changed': self.selected_flight,
            'on_delete_flight': self.delete_flight
        }
        self.builder.connect_signals(handlers)

        self.flights_list = self.builder.get_object('flightsList')

        # Met en place la liste déroulante avec le vol en avion par défaut
        self.flight_type = self.builder.get_object('flightType')
        self.create_type_list()
        self.flight_type.set_active(0)

        # Récupère les widgets du flight creator
        self.type = self.builder.get_object('flightType')
        self.id = self.builder.get_object('id')
        self.calendar = self.builder.get_object('calendar')

        self.add_plane_btn = self.builder.get_object('selectPlane')
        self.flight_rule = self.builder.get_object('flightRules')

        self.from_btn = self.builder.get_object('selectFrom')
        self.in_hours = self.builder.get_object('inHours')
        self.in_minutes = self.builder.get_object('inMinutes')

        self.to_btn = self.builder.get_object('selectTo')
        self.out_hours = self.builder.get_object('outHours')
        self.out_minutes = self.builder.get_object('outMinutes')

        self.day_hours = self.builder.get_object('dayFlightHours')
        self.day_minutes = self.builder.get_object('dayFlightMinutes')

        self.night_hours = self.builder.get_object('nightFlightHours')
        self.night_minutes = self.builder.get_object('nightFlightMinutes')

        self.takeoffs_nb = self.builder.get_object('takeoffsNb')
        self.landings_nb = self.builder.get_object('landingsNb')

        self.crew_view = self.builder.get_object('crewView')
        self.add_crew_btn = self.builder.get_object('addCrew')

        self.briefing = self.builder.get_object('note')
        self.briefing_buffer = self.builder.get_object('flightNote')


        # On recharge la listes des vols
        self.reload_flight_list()

        # La fenêtre principale
        self.window = self.builder.get_object('mainWindow')
        self.window.set_icon_from_file(config.icon_path)
        self.window.maximize()  # On met la fenêtre en grand directement

    def reload_flight_list(self):
        self.flights_list.clear()
        flights_path = []

        for flight_file in glob.glob('{}*{}'.format(config.logbook_folder,
                                                    config.flights_ext)):
            flights_path.append(flight_file)

        for flight_doc in flights_path:
            flight = Flight()
            flight.import_flight(flight_doc)
            icon = self.select_icon_type(flight.type)

            # On vérifie que l'avion existe bien (bug remonté par WinXaito)
            if os.path.isfile(flight.plane):
                plane = Plane()
                plane.import_plane(flight.plane)

                self.flights_list.append([icon, str(flight.id),
                                          flight.return_date(),
                                          plane.matriculation,
                                          flight.departure_airfield,
                                          flight.arrival_airfield,
                                          str(flight.takeoffs),
                                          str(flight.landings),
                                          flight.return_total_time(),
                                          flight.return_day_time(),
                                          flight.return_night_time()])
            else:
                self.flights_list.append([icon, str(flight.id),
                                          flight.return_date(),
                                          '',
                                          flight.departure_airfield,
                                          flight.arrival_airfield,
                                          str(flight.takeoffs),
                                          str(flight.landings),
                                          flight.return_total_time(),
                                          flight.return_day_time(),
                                          flight.return_night_time()])
        self.autoset_active()

    def select_icon_type(self, flight_type):
        if flight_type == 'plane':
            return GdkPixbuf.Pixbuf.new_from_file(config.plane)
        elif flight_type == 'simulator':
            return GdkPixbuf.Pixbuf.new_from_file(config.simulator)

    def create_type_list(self):
        type_list = self.builder.get_object('typeFlightList')
        plane = GdkPixbuf.Pixbuf.new_from_file(config.plane)
        simulator = GdkPixbuf.Pixbuf.new_from_file(config.simulator)

        type_list.append([plane, 'Avion', 'plane'])
        type_list.append([simulator, 'Simulateur', 'simulator'])

    def add_flight(self, button):
        pass

    def selected_flight(self, select):
        flight = self.return_flight_selected()
        if flight is not None:
            self.autoset_active()
            path = self.return_flight_path(self.return_flight_selected()[2])
            self.import_datas(path)

    def import_datas(self, flight_path):
        flight = Flight()
        flight.import_flight(flight_path)

        # Type de vol
        if flight.type == 'simulator':
            self.type.set_active(1)
        else:
            self.type.set_active(0) # Si c'est = à n'imp on met l'id 0

        # Identification du vol
        self.id.set_text(flight.id)

        # Date
        self.calendar.select_day(flight.return_day())
        self.calendar.select_month(flight.return_month(), flight.return_year())

        # Avion
        if flight.plane is not None:
            if os.path.isfile(flight.plane):
                plane = Plane()
                plane.import_plane(flight.plane)
                self.add_plane_btn.set_label(plane.matriculation)
            else:
                self.add_plane_btn.set_label('UNKNOWN')

        # Règle de vol
        if flight.flight_rule == 'ifr':
            self.flight_rule.set_active(1)
        else:
            self.flight_rule.set_active(0)

        # Terrain de départ
        if flight.departure_airfield is not None:
            self.from_btn.set_label(flight.departure_airfield)

        # Heure et minute de départ
        self.in_hours.set_value(flight.departure_hours)
        self.in_minutes.set_value(flight.departure_minutes)

        # Terrain d'arrivée
        if flight.departure_airfield is not None:
            self.to_btn.set_label(flight.arrival_airfield)

        # Heure et minute d'arrivée
        self.out_hours.set_value(flight.arrival_hours)
        self.out_minutes.set_value(flight.arrival_minutes)

        # Temps de vol de jour
        self.day_hours.set_value(flight.time_day_hours)
        self.day_minutes.set_value(flight.time_day_minutes)

        # Temps de vol de nuit
        self.night_hours.set_value(flight.time_night_hours)
        self.night_minutes.set_value(flight.time_night_minutes)

        # décollage et atterrissage
        self.takeoffs_nb.set_value(flight.takeoffs)
        self.landings_nb.set_value(flight.landings)

        # briefing
        self.briefing_buffer.set_text(flight.briefing)

    def autoset_active(self):
        if self.return_flight_selected() is not None:
            self.active_delete(True)
            self.active_flight_creator(True)
        else:
            self.active_delete(False)
            self.active_flight_creator(False)

    def active_delete(self, answer):
        delete_btn = self.builder.get_object('delete')
        delete_btn.set_sensitive(answer)

    def active_flight_creator(self, answer):
        self.type.set_sensitive(answer)
        self.id.set_sensitive(answer)
        self.calendar.set_sensitive(answer)

        self.add_plane_btn.set_sensitive(answer)
        self.flight_rule.set_sensitive(answer)

        self.from_btn.set_sensitive(answer)
        self.in_hours.set_sensitive(answer)
        self.in_minutes.set_sensitive(answer)

        self.to_btn.set_sensitive(answer)
        self.out_hours.set_sensitive(answer)
        self.out_minutes.set_sensitive(answer)

        self.day_hours.set_sensitive(answer)
        self.day_minutes.set_sensitive(answer)

        self.night_hours.set_sensitive(answer)
        self.night_minutes.set_sensitive(answer)

        self.takeoffs_nb.set_sensitive(answer)
        self.landings_nb.set_sensitive(answer)

        self.crew_view.set_sensitive(answer)
        self.add_crew_btn.set_sensitive(answer)
        self.briefing.set_sensitive(answer)

    def select_plane(self, button):
        """
        Ouvre le hangar afin de sélectionner un avion
        """
        selector = HangarDialog(True)
        response = selector.dialog.run()

        if response == 1:
            button.set_label(selector.return_selected())

        selector.dialog.destroy()

    def select_airfield(self, button):
        """
        Ouvre le sélecteur de terrain et met le label du boutton sur le
            terrain sélectionné.
        """
        selector = AirfieldSelectorDialog()
        response = selector.dialog.run()

        if response == 1:
            button.set_label(selector.return_airfield())

        selector.dialog.destroy()

    def return_flight_selected(self):
        cursor = self.builder.get_object('flightSelector')
        model, treeiter = cursor.get_selected()
        if treeiter is not None:
            return model[treeiter]
        else:
            return None

    def add_crew(self, button):
        pass

    def delete_flight(self, button):
        os.remove(self.return_flight_path(self.return_flight_selected()[2]))
        self.reload_flight_list()

    def return_flight_path(self, string):
        # On converti la date
        day, month, year = string.split('/')

        # On suppirme le 0 inutile ('02' -> '2')
        day = str(int(day))
        month = str(int(month))
        year = str(int(year))
        date = '-'.join((year, month, day))

        return '{}{}{}'.format(config.logbook_folder, date, config.flights_ext)

    def app_quit(self, widget):
        """
        Ferme la fenêtre
        """
        self.window.destroy()
