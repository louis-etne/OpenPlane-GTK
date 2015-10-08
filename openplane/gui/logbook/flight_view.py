#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk, GdkPixbuf
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
        builder.add_from_file('openplane/gui/logbook/flight_view.glade')

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


    def reload_flight(self):
        '''
        Recharge la liste des vols
        '''
        # On vide la liste des vols
        self.flight_list.clear()

        # La liste qui va contenir tous les chemins de fichier
        flights_path = []

        # On récupère tous les fichiers avec chemin en entier
        # Exemple : "/home/$USER/.../2015/9/1.opf"
        [flights_path.append(val) for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(config.logbook_folder)] for val in sublist]

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


    def select_icon_type(self, flight_type):
        '''
        Retourne l'icone du type de vol en fontion de celui-ci
        '''
        if flight_type == 'plane':
            return GdkPixbuf.Pixbuf.new_from_file(config.plane)
        elif flight_type == 'simulator':
            return GdkPixbuf.Pixbuf.new_from_file(config.simulator)


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
        '''
        # On récupère toutes les infos du vol
        path = self.return_flight_path()
        flight = self.return_flight_selected()

        # On regarde si le vol à un fichier associé
        if path is '':
            # Si non, on a juste à le supprimer de la liste
            self.flight_list.remove(flight)
        else:
            # Si oui, c'est plus complexe, car il faut aussi supprimer
            # les dossiers si ils sont vides
            working_directory = os.getcwd()

            # On sépare le chemin du fichier
            path, opf_flight = os.path.split(path)

            # On se déplace dans le dossier contenant le fichier
            os.chdir(path)
            # On supprime le fichier
            os.remove(opf_flight)
            # On récupère le nom du dossier actuel
            current_dir = os.path.relpath('.','..')

            # On remonte et on supprime si le dossier est vide
            while current_dir != 'logbook':
                # On remonte d'un dossier
                os.chdir('..')
                # On regarde si l'ancier dossier à des fichiers/dossiers
                # Si non, on le supprime,
                # Si oui, on le laisse
                if os.listdir(current_dir) == []:
                    os.rmdir(current_dir)

                # On récupère le dossier parent
                current_dir = os.path.relpath('.','..')

            # On retourne dans le dossier principal
            os.chdir(working_directory)
            # Et on recharge la liste des vols
            self.reload_flight()