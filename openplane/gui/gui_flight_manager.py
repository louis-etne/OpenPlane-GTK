#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane.core.Flight import *
from openplane.gui.gui_hangar import *
from openplane import config


class FlightManagerDialog:

    def __init__(self, flight_path=None):
        builder = Gtk.Builder()
        builder.add_from_file(config.flight_manager)

        handlers = {
            'on_close_clicked': self.app_quit,
            'on_save_clicked': self.on_save_clicked,
            'on_add_clicked': self.on_add_clicked
        }
        builder.connect_signals(handlers)

        # Widgets
        # Informations générales sur le vol
        self.date = builder.get_object('calendar')
        self.plane_chooser = builder.get_object('planeChooser')
        self.planes_list = builder.get_object('planeChooserList')
        self.update_planes_list()  # On créer la liste des avions
        self.plane_chooser.set_active(0)
        self.role = builder.get_object('role')
        self.type = builder.get_object('type')

        # Membres d'équipage
        self.members_day = builder.get_object('membersDay')
        self.members_night = builder.get_object('membersNight')
        self.members_hours = builder.get_object('membersHours')
        self.members_minutes = builder.get_object('membersMinuts')

        # Pilote monomoteur
        self.single_day = builder.get_object('singleDay')
        self.single_night = builder.get_object('singleNight')
        self.single_double = builder.get_object('singleDouble')
        self.single_captain = builder.get_object('singleCaptain')
        self.single_hours = builder.get_object('singleHours')
        self.single_minutes = builder.get_object('singleMinuts')

        # Pilote multimoteurs
        self.multi_day = builder.get_object('multiDay')
        self.multi_night = builder.get_object('multiNight')
        self.multi_double = builder.get_object('multiDouble')
        self.multi_captain = builder.get_object('multiCaptain')
        self.multi_copilot = builder.get_object('multiCopilot')
        self.multi_hours = builder.get_object('multiHours')
        self.multi_minutes = builder.get_object('multiMinuts')

        # IFR
        self.ifr_double = builder.get_object('ifrDouble')
        self.ifr_captain = builder.get_object('ifrCaptain')
        self.ifr_hours = builder.get_object('ifrHours')
        self.ifr_minutes = builder.get_object('ifrMinuts')

        # Autres
        self.simu_hours = builder.get_object('simuHours')
        self.simu_minutes = builder.get_object('simuMinuts')
        self.ifr_arrivals = builder.get_object('arrivals')

        # Observations
        self.observations = builder.get_object('observations')

        self.takeoff = builder.get_object('takeoff')
        self.landing = builder.get_object('landing')
        self.departure = builder.get_object('departure')
        self.arrival = builder.get_object('arrival')
        self.comments = builder.get_object('comments')

        self.dialog = builder.get_object('dialog')

        if flight_path is not None:
            self.import_flight(flight_path)

    def update_planes_list(self):
        '''
            Recharge la liste des avions afin de tenir compte des dernières
            modifications
        '''
        self.planes_list.clear()
        for plane_file in glob.glob('{}*{}'.format(config.planes_folder,
                                                   config.planes_ext)):
            plane = Plane()
            plane.import_plane(plane_file)

            self.planes_list.append([plane.matriculation])

    def on_add_clicked(self, button):
        '''
            Ouvre le hangar
        '''
        hangar = HangarDialog()
        hangar.dialog.run()
        self.update_planes_list()

    def on_save_clicked(self, button):
        '''
            Enregistre toutes les valeurs
        '''
        values = []
        values.append(self.save_date(self.date))
        values.append(self.save_plane(self.plane_chooser))
        values.append(self.role.get_active_id())
        values.append(self.type.get_text())

        values.append(self.members_day.get_active())
        values.append(self.members_hours.get_value_as_int())
        values.append(self.members_minutes.get_value_as_int())

        values.append(self.single_day.get_active())
        values.append(self.single_double.get_active())
        values.append(self.single_hours.get_value_as_int())
        values.append(self.single_minutes.get_value_as_int())

        values.append(self.multi_day.get_active())
        values.append(self.multi_double.get_active())
        values.append(self.multi_captain.get_active())
        values.append(self.multi_hours.get_value_as_int())
        values.append(self.multi_minutes.get_value_as_int())

        values.append(self.ifr_double.get_active())
        values.append(self.ifr_hours.get_value_as_int())
        values.append(self.ifr_minutes.get_value_as_int())

        values.append(self.simu_hours.get_value_as_int())
        values.append(self.simu_minutes.get_value_as_int())

        values.append(self.ifr_arrivals.get_value_as_int())

        start_iter = self.observations.get_start_iter()
        end_iter = self.observations.get_end_iter()
        values.append(self.observations.get_text(start_iter, end_iter, True))

        values.append(self.takeoff.get_value_as_int())
        values.append(self.landing.get_value_as_int())
        values.append(self.departure.get_text())
        values.append(self.arrival.get_text())

        start_iter = self.comments.get_start_iter()
        end_iter = self.comments.get_end_iter()
        values.append(self.comments.get_text(start_iter, end_iter, True))

        flight = Flight(values)
        flight.save_flight()

        self.app_quit()

    def save_date(self, calendar):
        year, month, day = calendar.get_date()
        month += 1  # Normalement de 0 à 11, maintenant de 1 à 12
        return '-'.join([str(year), str(month), str(day)])

    def save_plane(self, plane_chooser):
        plane_name = plane_chooser.get_active_id()
        return '{}{}{}'.format(config.planes_folder, plane_name,
                               config.planes_ext)

    def import_flight(self, flight_path):
        '''
            Importe un vol dans la fenêtre
        '''
        flight = Flight()
        flight.import_flight(flight_path)

        plane = Plane()
        plane.import_plane(flight.plane)

        year, month, day = flight.date.split('-')

        self.date.select_day(int(day))
        self.date.select_month(int(month) - 1, int(year))


        self.plane_chooser.set_active_id(plane.matriculation)
        self.role.set_active_id(flight.role)
        self.type.set_text(flight.type)

        # Membres d'équipage
        self.members_night.set_active(not flight.members_day)
        self.members_hours.set_value(flight.members_hours)
        self.members_minutes.set_value(flight.members_minutes)

        # Pilote monomoteur
        self.single_night.set_active(not flight.single_engine_day)
        self.single_captain.set_active(not flight.single_engine_double)
        self.single_hours.set_value(flight.single_engine_hours)
        self.single_minutes.set_value(flight.single_engine_minutes)

        # Pilote multimoteurs
        self.multi_night.set_active(not flight.multi_engines_day)
        if flight.multi_engines_double:
            self.multi_double.set_active(True)
        elif flight.multi_engines_captain:
            self.multi_captain.set_active(True)
        else:
            self.multi_copilot.set_active(True)
        self.multi_hours.set_value(flight.multi_engines_hours)
        self.multi_minutes.set_value(flight.multi_engines_minutes)

        # IFR
        self.ifr_captain.set_active(not flight.ifr_double)
        self.ifr_hours.set_value(flight.ifr_hours)
        self.ifr_minutes.set_value(flight.ifr_minutes)

        # Autres
        self.simu_hours.set_value(flight.simulation_hours)
        self.simu_minutes.set_value(flight.simulation_minutes)
        self.ifr_arrivals.set_value(flight.ifr_arrivals)

        # Commentaires
        self.observations.set_text(flight.observations)

        self.takeoff.set_value(flight.takeoff)
        self.landing.set_value(flight.landing)
        self.departure.set_text(flight.departure)
        self.arrival.set_text(flight.arrival)
        self.comments.set_text(flight.comments)

        self.dialog.set_title(text.edit_flight.format(day, month, year))

    def app_quit(self, *args):
        '''
            Détruit la fenêtre de dialogue actuelle
        '''
        self.dialog.destroy()
