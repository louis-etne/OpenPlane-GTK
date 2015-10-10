#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk, GdkPixbuf
from pathlib import Path
import datetime
import time
import os

from openplane import config
from openplane.core.Flight import *
from openplane.core.Plane import *
from openplane.gui.logbook.flight_editor import *


class FlightView(Gtk.Box):

    def __init__(self, parent):
        Gtk.Box.__init__(self)
        # On défini l'orientation pour que le layout soit horizontal
        self.set_orientation(0)

        builder = Gtk.Builder()
        builder.add_from_file(config.flight_view)

        # On récupère le layout principal qu'on attache ensuite à cette classe
        # celle-ci se fait ensuite attachée dans le logbook
        main_layout = builder.get_object('FlightView')
        self.pack_start(main_layout, True, True, 0)

        # On récupère le parent
        self.logbook = parent

        # On ajoute aussi l'éditeur de vol
        self.flight_editor = FlightEditor(self)
        self.pack_start(self.flight_editor, True, True, 0)

        # On définit les handlers et on les envoie au builder
        handlers = {
            'on_cursor_changed': self.cursor_changed,
            'on_save': self.on_save,
            'on_add_flight': self.add_flight,
            'on_delete_flight': self.delete_flight
            }
        builder.connect_signals(handlers)

        # On récupère le curseur
        self.cursor = builder.get_object('flightCursor')

        # On charge les boutons
        self.save = builder.get_object('save')
        self.delete = builder.get_object('delete')

        # On récupère la barre de status et la vue
        self.flight_view = builder.get_object('flightsView')
        self.status_bar = builder.get_object('status')

        # On récupère la liste des vols
        self.flight_list = builder.get_object('flightList')
        # Et on la recharge
        self.reload_flight()


    def cursor_changed(self, cursor):
        '''
        Est appellée quand un vol est sélectionné/déselectionné
        '''
        flight = self.return_flight_selected()

        if flight is not None:
            # L'éditeur de vol s'active
            self.flight_editor.set_widgets_sensitive(True)

            # On regarde si le vol a un chemin
            flight_path = self.return_flight_path()

            if flight_path == '':
                 # C'est un nouvel avion
                self.flight_editor.import_flight()
            else:
                # On lui envoie le chemin du vol
                self.flight_editor.import_flight(flight_path)

            # Et on active le bouton pour sauvegarder et pour supprimer
            self.save.set_sensitive(True)
            self.delete.set_sensitive(True)
        else:
            self.flight_editor.set_widgets_sensitive(False)
            self.save.set_sensitive(False)
            self.delete.set_sensitive(False)


    def return_flight_selected(self):
        '''
        Retourne un treeiter contenant le vol sélectionné
        '''
        model, treeiter = self.cursor.get_selected()
        # On vérifie qu'il ne soit pas nul
        if treeiter is not None:
            return treeiter
        else:
            return None


    def reload_flight(self, date='all', day='all', rule='all', f_type='all'):
        '''
        Recharge la liste des vols avec les arguments
        '''
        # On vide la liste des vols
        self.flight_list.clear()

        # La liste qui va contenir tous les chemins de fichier
        flights_path = []

        # On récupère tous les fichiers avec chemin en entier
        # Exemple : "/home/$USER/.../2015/9/1.opf"
        [flights_path.append(val) for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(config.logbook_folder)] for val in sublist]

        for i in range(len(flights_path) - 1, -1, -1):
            flight = Flight()
            flight.import_flight(flights_path[i])

            if date == 'week' and not self.is_in_week(flight):
                del flights_path[i]
                # On passe à la prochaine itération
                continue
            elif date == 'month' and not self.is_in_month(flight):
                del flights_path[i]
                # On passe à la prochaine itération
                continue
            elif date == '6months' and not self.is_in_6months(flight):
                del flights_path[i]
                # On passe à la prochaine itération
                continue
            elif date == 'year' and not self.is_in_year(flight):
                del flights_path[i]
                # On passe à la prochaine itération
                continue

            # On vérifie si on veut les vols de jour, de nuits ou peu importe
            if day == 'day':
                if flight.time_day_hours < flight.time_night_hours:
                    del flights_path[i]
                    # On passe à la prochaine itération
                    continue
                elif flight.time_day_hours == flight.time_night_hours:
                    if flight.time_day_minutes < flight.time_night_minutes:
                        del flights_path[i]
                        # On passe à la prochaine itération
                        continue
            elif day == 'night':
                if flight.time_night_hours < flight.time_day_hours:
                    del flights_path[i]
                    # On passe à la prochaine itération
                    continue
                elif flight.time_night_hours == flight.time_day_hours:
                    if flight.time_night_minutes < flight.time_day_minutes:
                        del flights_path[i]
                        # On passe à la prochaine itération
                        continue

            # On vérifie la règle de vol
            if rule == 'vfr' and flight.flight_rule == 'IFR':
                del flights_path[i]
                # On passe à la prochaine itération
                continue
            elif rule == 'ifr' and flight.flight_rule == 'VFR':
                del flights_path[i]
                # On passe à la prochaine itération
                continue

            # On vérifie le type de vol
            if f_type == 'plane' and flight.type != 'plane':
                del flights_path[i]
                # On passe à la prochaine itération
                continue
            elif f_type == 'simulator' and flight.type != 'simulator':
                del flights_path[i]
                # On passe à la prochaine itération
                continue
            elif f_type == 'model' and flight.type != 'model':
                del flights_path[i]
                # On passe à la prochaine itération
                continue

        # Pour chaque fichier, on en créer un vol
        for flight_doc in flights_path:
            flight = Flight()
            flight.import_flight(flight_doc)
            icon = self.select_icon_type(flight.type)

            # On vérifie que l'avion existe bien (bug remonté par WinXaito)
            if flight.plane is not None and os.path.isfile(flight.plane):
                plane = Plane()
                plane.import_plane(flight.plane)

                self.flight_list.append([icon, flight.id,
                                         flight.return_date(),
                                         plane.matriculation,
                                         flight.departure_airfield,
                                         flight.arrival_airfield,
                                         int(flight.takeoffs),
                                         int(flight.landings),
                                         flight.return_total_time(),
                                         flight.return_day_time(),
                                         flight.return_night_time(),
                                         flight.flight_rule,
                                         flight_doc])
            else:
                self.flight_list.append([icon, flight.id,
                                         flight.return_date(),
                                         'UNKNOW',
                                         flight.departure_airfield,
                                         flight.arrival_airfield,
                                         int(flight.takeoffs),
                                         int(flight.landings),
                                         flight.return_total_time(),
                                         flight.return_day_time(),
                                         flight.return_night_time(),
                                         flight.flight_rule,
                                         flight_doc])
        # On recharge le footer aussi
        self.update_footer()


    def select_icon_type(self, flight_type):
        '''
        Retourne l'icone du type de vol en fontion de celui-ci
        '''
        if flight_type == 'plane':
            return GdkPixbuf.Pixbuf.new_from_file(config.plane)
        elif flight_type == 'simulator':
            return GdkPixbuf.Pixbuf.new_from_file(config.simulator)
        elif flight_type == 'model':
            return GdkPixbuf.Pixbuf.new_from_file(config.model)


    def return_flight_path(self):
        '''
        Retourne le chemin du fichier du vol sélectionné
        '''
        model, treeiter = self.cursor.get_selected()

        # On vérifie qu'il ne soit pas nul
        if treeiter is not None:
            # On sélectionne la dernière colonne
            # (celle qui contient le chemin)
            return model.get_value(treeiter, 12)
        else:
            return None


    def on_save(self, button):
        '''
        Quand le bouton sauvegarder est pressé
        '''
        # On sauvegarde les valeurs
        path = self.return_flight_path()

        if path != '':
            self.flight_editor.save_flight(path)
        else:
            self.flight_editor.save_flight()

        # Et on recharge la liste
        self.reload_flight()


    def add_flight(self, button):
        '''
        Ajoute un vol
        '''
        # On récupère la date du jour
        date = time.strftime('%d/%m/%Y')
        self.flight_list.append([None, '', date, 'UNKNOW', '', '', None, None,
                                 '', '', '', '', ''])


    def delete_flight(self, button):
        '''
        Supprime le vol et les fichier correspondant
        Voir : https://zestedesavoir.com/forums/sujet/4223/suppression-de-fichiersdossiers/

        Améloration proposée par nohar
        '''
        # On récupère le lien vers le fichier du vol
        path = self.return_flight_path()
        # On le retire de la liste
        self.flight_list.remove(self.return_flight_selected())

        # Si le fichier existe vraiment
        if path != '':
            file_path = Path(path)
            if file_path.exists():
                # supprime le fichier
                file_path.unlink()

            for parent, _ in zip(file_path.parents, range(3)):
                # On itère sur l'arborescence parente
                # En ne remontant pas plus de 3 niveaux
                try:
                    parent.rmdir()
                except OSError:
                    # Le dossier n'est pas vide.
                    break

        # Et on recharge la liste des vols
        self.reload_flight()


    def update_footer(self):
        '''
        Met à jour la barre de status
        '''
        # On récupère les différentes valeurs
        day_time = self.get_day_time()
        night_time = self.get_night_time()
        total_time = self.get_total_time(day_time, night_time)
        landings = self.get_total_landings()
        flights_nb = self.get_flights_nb()

        # On charge le texte
        label = '{} heure(s), '\
                '{} heure(s) de nuit, '\
                '{} heure(s) de jour et '\
                '{} atterrissage(s) pour '\
                '{} vol(s)'.format(total_time, night_time, day_time,
                                   landings, flights_nb)

        # On met à jour le label avec
        self.status_bar.set_label(label)


    def get_flights_nb(self):
        '''
        Retourne le nombre de vols dans la vue
        '''
        model = self.flight_view.get_model()
        counter = 0

        for flight in model:
            counter += 1

        return counter


    def get_total_landings(self):
        '''
        Retourne le nombre d'atterrissage de la vue
        '''
        model = self.flight_view.get_model()
        total = 0

        for flight in model:
            total += int(flight[7])

        return total


    def format_timedelta(self, td):
        '''
        Retourne le nombre d'heure sans compter les jours :
        Normalement : 13h + 23h -> 1j et 12h
        Maintenant : 13h + 23h -> 36h
        Prend en compte les secondes (mod 60)
        '''
        minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
        hours, minutes = divmod(minutes, 60)
        return int(hours), int(minutes)


    def format_time(self, hours, minutes):
        '''
        Retourne l'heure parfaitement formaté :
        03:05
        '''
        hours = int(hours)
        minutes = int(minutes)

        if hours < 10:
            hours = '0{}'.format(hours)

        if minutes < 10:
            minutes = '0{}'.format(minutes)

        return ':'.join((str(hours), str(minutes)))


    def get_day_time(self):
        '''
        Retourne le nombre d'heures de vol de jour de la vue
        '''
        model = self.flight_view.get_model()
        total = datetime.timedelta(hours=0, minutes=0)

        for flight in model:
            hours, minutes = flight[9].split(':')
            td = datetime.timedelta(hours=int(hours), minutes=int(minutes))

            total += td

        total_hours, total_minutes = self.format_timedelta(total)
        return self.format_time(total_hours, total_minutes)


    def get_night_time(self):
        '''
        Retourne le nombre d'heures de vol de nuit de la vue
        '''
        model = self.flight_view.get_model()
        total = datetime.timedelta(hours=0, minutes=0)

        for flight in model:
            hours, minutes = flight[10].split(':')
            td = datetime.timedelta(hours=int(hours), minutes=int(minutes))

            total += td

        total_hours, total_minutes = self.format_timedelta(total)
        return self.format_time(total_hours, total_minutes)


    def get_total_time(self, day_time, night_time):
        '''
        Calcule et retourne le temps de vol total de la vue
        '''
        day_hours, day_minutes = day_time.split(':')
        day_hours = int(day_hours)
        day_minutes = int(day_minutes)

        night_hours, night_minutes = night_time.split(':')
        night_hours = int(night_hours)
        night_minutes = int(night_minutes)

        day = datetime.timedelta(hours=day_hours, minutes=day_minutes)
        night = datetime.timedelta(hours=night_hours, minutes=night_minutes)

        total = day + night
        total_hours, total_minutes = self.format_timedelta(total)

        return self.format_time(total_hours, total_minutes)


    def is_in_week(self, flight):
        '''
        Retourne true si la date fait partie des 7 derniers jours
        '''
        year, month, day = flight.date.split('-')
        day = int(day)
        month = int(month) + 1  # On décalle le mois d'un cran
        year = int(year)
        flight = datetime.date(year, month, day)

        # Pareil avec la date du jour
        now = datetime.date.today()
        operand = datetime.timedelta(days=7)

        if flight >= now - operand:
            return True
        else:
            return False


    def is_in_month(self, flight):
        '''
        Retourne True si la date est comprise dans les 28 derniers jours
        '''
        year, month, day = flight.date.split('-')
        day = int(day)
        month = int(month) + 1  # On décalle le mois d'un cran
        year = int(year)
        flight = datetime.date(year, month, day)

        # Pareil avec la date du jour
        now = datetime.date.today()
        operand = datetime.timedelta(28)

        if flight >= now - operand:
            return True
        else:
            return False


    def is_in_6months(self, flight):
        '''
        Retourne True si la date est comprise dans les 6 derniers mois
        '''
        year, month, day = flight.date.split('-')
        day = int(day)
        month = int(month) + 1  # On décalle le mois d'un cran
        year = int(year)
        flight = datetime.date(year, month, day)

        # Pareil avec la date du jour
        now = datetime.date.today()
        operand = datetime.timedelta(6 * 365/12)

        if flight >= now - operand:
            return True
        else:
            return False


    def is_in_year(self, flight):
        '''
        Retourne True si la date est comprise dans l'année
        '''
        year, month, day = flight.date.split('-')
        day = int(day)
        month = int(month) + 1  # On décalle le mois d'un cran
        year = int(year)
        flight = datetime.date(year, month, day)

        # Pareil avec la date du jour
        now = datetime.date.today()
        operand = datetime.timedelta(365)

        if flight >= now - operand:
            return True
        else:
            return False

