#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane.gui.gui_plane_manager import *
from openplane import config
import shutil
import json
import glob
import os


class HangarDialog():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file(config.hangar)

        handlers = {
            'on_close_clicked': self.app_quit,
            'on_new_clicked': self.on_new_clicked,
            'on_import_clicked': self.on_import_clicked,
            'on_select_changed': self.on_select_changed,
        }

        builder.connect_signals(handlers)

        self.select = builder.get_object('planeSelect')

        self.btn_edit = builder.get_object('edit')
        self.btn_edit.connect('clicked', self.on_edit_clicked, self.select)

        self.btn_delete = builder.get_object('delete')
        self.btn_delete.connect('clicked', self.on_delete_clicked, self.select)

        self.planes_list = Gtk.ListStore(str, str)
        self.update_file_list()

        tree = builder.get_object('planesView')
        tree.set_model(self.planes_list)

        column_name = Gtk.TreeViewColumn('Immatriculation')
        matriculation = Gtk.CellRendererText()
        column_name.pack_start(matriculation, True)
        column_name.add_attribute(matriculation, 'text', 0)

        column_path = Gtk.TreeViewColumn('Chemin du fichier')
        file_path = Gtk.CellRendererText()
        file_path.props.style = 2
        column_path.pack_start(file_path, True)
        column_path.add_attribute(file_path, 'text', 1)

        tree.append_column(column_name)
        tree.append_column(column_path)

        self.dialog = builder.get_object('dialog')
        self.dialog.set_modal(True)
        self.dialog.set_icon_from_file(config.logo_path)

    def update_file_list(self, btn=None):
        self.planes_list.clear()
        planes_path = []

        for plane_file in glob.glob('{}*.json'.format(config.planes_folder)):
            planes_path.append(plane_file)

        for plane in planes_path:
            plane_name = os.path.basename(plane)
            plane_name = os.path.splitext(plane_name)[0]
            self.planes_list.append([plane_name, plane])

    def on_select_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            if not self.btn_edit.get_sensitive():
                self.btn_edit.set_sensitive(True)

            if not self.btn_delete.get_sensitive():
                self.btn_delete.set_sensitive(True)
        else:
            self.btn_edit.set_sensitive(False)
            self.btn_delete.set_sensitive(False)

    def on_new_clicked(self, button):
        add_plane = PlanesManagerDialog()
        add_plane.dialog.run()
        self.update_file_list()

    def on_edit_clicked(self, button, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            edit_plane = PlanesManagerDialog(model[treeiter][1])
            edit_plane.dialog.run()
            self.update_file_list()

    def on_import_clicked(self, button):
        dialog = Gtk.FileChooserDialog('Sélectionnez le fichier', self.dialog,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN,
                                        Gtk.ResponseType.OK))
        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            plane_name = self.get_plane_name(file_path)

            new_path = '{}{}.json'.format(config.planes_folder, plane_name)

            shutil.copy(file_path, new_path)

            self.update_file_list()
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def get_plane_name(self, filepath):
        with open(filepath, 'r') as reader:
            datas = json.load(reader)

            return datas['Immatriculation'].upper()

    def add_filters(self, dialog):
        filter_json = Gtk.FileFilter()
        filter_json.set_name("Fichiers JSON")
        filter_json.add_pattern("*.json")
        dialog.add_filter(filter_json)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Tous les fichiers")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_delete_clicked(self, button, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            os.remove(model[treeiter][1])
            self.update_file_list()

    def app_quit(self, *args):
        self.dialog.destroy()
