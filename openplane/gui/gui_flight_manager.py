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
        self.members_hours = builder.get_object('membersHours')
        self.members_minuts = builder.get_object('membersMinuts')

        # Pilote monomoteur
        self.single_day = builder.get_object('singleDay')
        self.single_double = builder.get_object('singleDouble')
        self.single_hours = builder.get_object('singleHours')
        self.single_minuts = builder.get_object('singleMinuts')

        # Pilote multimoteurs
        self.multi_day = builder.get_object('multiDay')
        self.multi_double = builder.get_object('multiDouble')
        self.multi_captain = builder.get_object('multiCaptain')
        self.multi_hours = builder.get_object('multiHours')
        self.multi_minuts = builder.get_object('multiMinuts')

        # IFR
        self.ifr_double = builder.get_object('ifrDouble')
        self.ifr_hours = builder.get_object('ifrHours')
        self.ifr_minuts = builder.get_object('ifrMinuts')

        # Autres
        self.simu_hours = builder.get_object('simuHours')
        self.simu_minuts = builder.get_object('simuMinuts')
        self.ifr_arrivals = builder.get_object('arrivals')

        # Commentaires
        self.comments = builder.get_object('comments')

        self.dialog = builder.get_object('dialog')

    def time_gui2text(self, hours, minuts):
        '''
            Converti le temps renvoyé par la gui en un format texte
            hh:mm
        '''
        if hours < 10:
            hours = '0' + str(hours)
        if minuts < 10:
            minuts = '0' + str(minuts)
        return ':'.join([str(hours), str(minuts)])

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

        if self.members_day.get_active():
            values.append(self.time_gui2text(self.members_hours.get_value_as_int(),
                                             self.members_minuts.get_value_as_int()))
            values.append('00:00')
        else:
            values.append('00:00')
            values.append(self.time_gui2text(self.members_hours.get_value_as_int(),
                                             self.members_minuts.get_value_as_int()))

        if self.single_day.get_active():
            if self.single_double.get_active():
                values.append(self.time_gui2text(self.single_hours.get_value_as_int(),
                                                 self.single_minuts.get_value_as_int()))
                values.append('00:00')
            else:
                values.append('00:00')
                values.append(self.time_gui2text(self.single_hours.get_value_as_int(),
                                                 self.single_minuts.get_value_as_int()))
            values.append('00:00')
            values.append('00:00')
        else:
            values.append('00:00')
            values.append('00:00')
            if self.single_double.get_active():
                values.append(self.time_gui2text(self.single_hours.get_value_as_int(),
                                                 self.single_minuts.get_value_as_int()))
                values.append('00:00')
            else:
                values.append('00:00')
                values.append(self.time_gui2text(self.single_hours.get_value_as_int(),
                                                 self.single_minuts.get_value_as_int()))

        if self.multi_day.get_active():
            if self.multi_double.get_active():
                values.append(self.time_gui2text(self.multi_hours.get_value_as_int(),
                                                 self.multi_minuts.get_value_as_int()))
                values.append('00:00')
                values.append('00:00')
            elif self.multi_captain.get_active():
                values.append('00:00')
                values.append(self.time_gui2text(self.multi_hours.get_value_as_int(),
                                                 self.multi_minuts.get_value_as_int()))
                values.append('00:00')
            else:
                values.append('00:00')
                values.append('00:00')
                values.append(self.time_gui2text(self.multi_hours.get_value_as_int(),
                                                 self.multi_minuts.get_value_as_int()))
            values.append('00:00')
            values.append('00:00')
            values.append('00:00')
        else:
            values.append('00:00')
            values.append('00:00')
            values.append('00:00')
            if self.multi_double.get_active():
                values.append(self.time_gui2text(self.multi_hours.get_value_as_int(),
                                                 self.multi_minuts.get_value_as_int()))
                values.append('00:00')
                values.append('00:00')
            elif self.multi_captain.get_active():
                values.append('00:00')
                values.append(self.time_gui2text(self.multi_hours.get_value_as_int(),
                                                 self.multi_minuts.get_value_as_int()))
                values.append('00:00')
            else:
                values.append('00:00')
                values.append('00:00')
                values.append(self.time_gui2text(self.multi_hours.get_value_as_int(),
                                                 self.multi_minuts.get_value_as_int()))

        if self.ifr_double.get_active():
            values.append(self.time_gui2text(self.ifr_hours.get_value_as_int(),
                                             self.ifr_minuts.get_value_as_int()))
            values.append('00:00')
        else:
            values.append('00:00')
            values.append(self.time_gui2text(self.ifr_hours.get_value_as_int(),
                                             self.ifr_minuts.get_value_as_int()))

        values.append(self.time_gui2text(self.simu_hours.get_value_as_int(),
                                         self.simu_minuts.get_value_as_int()))
        values.append(self.ifr_arrivals.get_value_as_int())

        start_iter = self.comments.get_start_iter()
        end_iter = self.comments.get_end_iter()

        values.append(self.comments.get_text(start_iter, end_iter, True))

        flight = Flight(values)
        flight.save_flight()

        self.app_quit()

    def save_date(self, calendar):
        year, mounth, day = calendar.get_date()
        mounth += 1  # Normalement de 0 à 11, maintenant de 1 à 12
        return '-'.join([str(year), str(mounth), str(day)])

    def save_plane(self, plane_chooser):
        plane_name = plane_chooser.get_active_id()
        return '{}{}{}'.format(config.planes_folder, plane_name,
                               config.planes_ext)

    def app_quit(self, *args):
        '''
            Détruit la fenêtre de dialogue actuelle
        '''
        self.dialog.destroy()
