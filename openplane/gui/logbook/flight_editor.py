#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk, GdkPixbuf
import time
import os

from openplane import config
from openplane.gui.gui_airfields_selector import *
from openplane.gui.gui_crew_adder import *
from openplane.gui.gui_hangar import *
from openplane.core.Flight import *
from openplane.core.Plane import *


class FlightEditor(Gtk.Box):

    def __init__(self, parent):
        Gtk.Box.__init__(self)

        builder = Gtk.Builder()
        builder.add_from_file('openplane/gui/logbook/flight_editor.glade')

        # On récupère le layout principal qu'on attache
        #ensuite à cette classe
        main_layout = builder.get_object('FlightEditor')
        self.pack_start(main_layout, True, True, 0)

        # On récupère tous les widgets de la fenêtre
        self.get_widgets(builder)
        # Et on les figes
        self.set_widgets_sensitive(False)

        # On charge la liste des types de vol
        self.load_flight_type_values(builder)

        # On récupère le parent
        self.flight_view = parent
        # On en déduis la fenêtre principale
        self.main_window = self.flight_view.logbook.window

        # Pour finir, on définit tous les handlers
        handlers = {
            'on_add_plane': self.select_plane,
            'on_add_airfield': self.select_airfield,
            'on_add_crew': self.add_crew,
            'on_delete_crew': self.delete_crew,
            'on_crewCursor_changed': self.crew_cursor_changed
        }
        # Et on les connecte grâce au builder
        builder.connect_signals(handlers)


    def get_widgets(self, builder):
        '''
        Récupère tous les widgets
        '''
        self.type = builder.get_object('flightType')
        self.id = builder.get_object('id')

        self.calendar = builder.get_object('calendar')
        self.set_date_on_today()

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
        self.del_crew_btn = builder.get_object('delCrew')
        self.crew_list = builder.get_object('crewList')
        self.crew_cursor = builder.get_object('crewCursor')

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


    def set_date_on_today(self):
        '''
        Règle le calendrier sur la date du jour
        '''
        # On récupère la date du jour
        date = time.strftime('%-d-%-m-%Y')
        # On la split en 3
        day, month, year = date.split('-')
        # On règle le calendrier
        self.calendar.select_day(int(day))
        self.calendar.select_month(int(month) - 1, int(year))


    def import_flight(self, path=None):
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
        else:
            # C'est un nouvel avion, on remet donc les valeurs à 0
            self.type.set_active_id('Plane')
            self.id.set_text('')
            self.set_date_on_today()

            self.add_plane_btn.set_label(Gtk.STOCK_ADD)
            self.flight_rule.set_active_id('VFR')

            self.from_btn.set_label(Gtk.STOCK_ADD)
            self.departure_hours.set_value(0)
            self.departure_minutes.set_value(0)

            self.to_btn.set_label(Gtk.STOCK_ADD)
            self.arrival_hours.set_value(0)
            self.arrival_minutes.set_value(0)

            self.day_hours.set_value(0)
            self.day_minutes.set_value(0)

            self.night_hours.set_value(0)
            self.night_minutes.set_value(0)

            self.takeoffs_nb.set_value(1)
            self.landings_nb.set_value(1)

            self.set_crew(None)

            self.briefing_buffer.set_text('')


    def set_date(self, flight):
        '''
        Règle le calendrier sur la date entrée (flight.date)
        '''
        # On récupère le jour, le mois et l'année
        day = flight.return_day()
        month = flight.return_month()
        year = flight.return_year()

        # On règle le calendrier
        self.calendar.select_day(day)
        self.calendar.select_month(month, year)


    def set_plane(self, flight):
        '''
        Met le label du bouton de sélection d'avion sur le nom
        de l'avion si existant, sur UNKNOWN si non
        '''
        if flight is None:
            self.add_plane_btn.set_label('UNKNOWN')
        else:
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
        if flight is None:
            self.crew_list.clear()
        else:
            # Rien ne sert de nettoyer la liste si il n'y a pas d'équipage
            if len(flight.crew) > 0:
                self.crew_list.clear()

                for person in flight.crew:
                    # Valeurs possibles :
                    # Pilot, Captain, Co-pilot, Passenger et Instructor
                    role = self.convert_crew_role(person[1])

                    self.crew_list.append([person[0], role])


    def convert_crew_role(self, role):
        '''
        Converti le role de l'anglais vers le français
        '''
        if role == 'Captain':
            return 'Commandant de bord'
        elif role == 'Co-pilot':
            return 'Co-pilote'
        elif role == 'Passenger':
            return 'Passager'
        elif role == 'Instructor':
            return 'Instructeur'
        else:
            return 'Pilote'


    def select_plane(self, button):
        '''
        Ouvre le hangar afin de sélectionner un avion
        '''
        selector = HangarDialog(True)
        selector.dialog.set_transient_for(self.main_window)
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
        selector.dialog.set_transient_for(self.main_window)
        response = selector.dialog.run()

        if response == 1:
            button.set_label(selector.return_airfield())

        selector.dialog.destroy()


    def add_crew(self, button):
        '''
        Ouvre le CrewAdder afin d'ajouter une personne
        '''
        crew_adder = CrewAdderDialog()
        crew_adder.dialog.set_transient_for(self.main_window)
        response = crew_adder.dialog.run()

        if response == 1:
            # On récupère les valeurs
            name, role = crew_adder.return_value()

            # On les ajoutes à la liste
            self.crew_list.append([name, self.convert_crew_role(role)])

        crew_adder.dialog.destroy()


    def delete_crew(self, cursor):
        '''
        Supprime le passager sélectionné de la GtkView de l'équipage
        '''
        model, treeiter = cursor.get_selected()
        # On supprime le passager de la liste, la View se mettre à
        # jour toute seule
        self.crew_list.remove(treeiter)


    def crew_cursor_changed(self, cursor):
        '''
        Quand le curseur de la GtkView des passagers est changée
        '''
        model, treeiter = cursor.get_selected()

        if treeiter is not None:
            # On active le bouton pour supprimer un passager
            self.del_crew_btn.set_sensitive(True)
        else:
            self.del_crew_btn.set_sensitive(False)


    def save_flight(self, path=None):
        '''
        Récupère les valeurs des widgets et les envoie dans la classe
        Flight

        Si path == None, ça signifie que c'est un nouveau vol, autrement,
        c'est un vol modifié
        '''

        values = []
        # On récupère le type de vol
        values.append(self.type.get_active_id())
        # L'ID du vol
        values.append(self.id.get_text())
        # La date
        values.append(self.get_date())
        # L'avion
        values.append(self.get_plane())
        # La règle de vol
        values.append(self.flight_rule.get_active_id())
        # L'aérodrome de départ
        values.append(self.get_label(self.from_btn))
        # L'heure de départ
        values.append(self.departure_hours.get_value())
        values.append(self.departure_minutes.get_value())
        # L'aérodrome d'arrivé
        values.append(self.get_label(self.to_btn))
        # L'heure d'arrivé
        values.append(self.arrival_hours.get_value())
        values.append(self.arrival_minutes.get_value())
        # Nombre d'heures le jour
        values.append(self.day_hours.get_value())
        values.append(self.day_minutes.get_value())
        # Nombre d'heures la nuit
        values.append(self.night_hours.get_value())
        values.append(self.night_minutes.get_value())
        # Nombre de décollages & atterrissage
        values.append(self.takeoffs_nb.get_value())
        values.append(self.landings_nb.get_value())
        # Équipage
        values.append(self.get_crew())
        # Briefing
        values.append(self.get_briefing())

        flight = Flight(values)

        # Si on doit écraser ou pas
        if path is not None:
            flight.save_flight(path)
        else:
            flight.save_flight()


    def get_date(self):
        '''
        Retourne la date du calendrier sous la forme 'YYYY-MM-JJ'
        '''
        # On récupère les trois valeurs
        year, month, day = self.calendar.get_date()
        return '-'.join((str(year), str(month), str(day)))


    def get_plane(self):
        '''
        Retourne le chemin de l'avion
        '''
        label = self.add_plane_btn.get_label()

        if label == 'gtk-add':
            return ''
        else:
            return '{}{}{}'.format(config.planes_folder, label,
                                   config.planes_ext)


    def get_label(self, button):
        '''
        Retourne le label du boutton
        '''
        label = button.get_label()

        if label == 'gtk-add':
            return ''
        else:
            return label


    def get_crew(self):
        '''
        Retourne sous forme d'une liste l'équipage ayant participé au vol
        [['Foo Bar', 'Captain'], ['Bar Foo', 'Passenger']]
        '''
        model = self.crew_view.get_model()
        crew_list = []

        for person in model:
            values = []
            for entry in person:
                values.append(entry)

            crew_list.append(values)

        # Et on retourne la liste finale
        return crew_list


    def get_briefing(self):
        '''
        Retourne le briefing
        '''
        start_iter = self.briefing_buffer.get_start_iter()
        end_iter = self.briefing_buffer.get_end_iter()

        return self.briefing_buffer.get_text(start_iter, end_iter, True)