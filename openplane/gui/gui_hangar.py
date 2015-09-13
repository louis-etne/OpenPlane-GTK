#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane.gui.gui_plane_manager import *
import shutil
import json
import glob
import os


class HangarWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Hangar')

        self.set_border_width(10)

        main_layout = Gtk.Grid()

        main_layout.set_row_spacing(6)
        main_layout.set_column_spacing(6)
        main_layout.set_column_homogeneous(True)
        main_layout.set_row_homogeneous(True)

        self.store = Gtk.ListStore(str, str)
        self.update_file_list()

        tree = Gtk.TreeView(self.store)

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

        select = tree.get_selection()

        main_layout.attach(tree, 0, 0, 4, 6)

        # Btn
        btn_new = Gtk.Button(label='Nouveau')
        btn_new.connect('clicked', self.on_new_pressed)
        main_layout.attach(btn_new, 4, 0, 1, 1)

        self.btn_edit = Gtk.Button(label='Modifier')
        self.btn_edit.connect('clicked', self.on_edit_pressed, select)
        self.btn_edit.set_sensitive(False)
        main_layout.attach(self.btn_edit, 4, 1, 1, 1)

        btn_import = Gtk.Button(label='Importer')
        btn_import.connect('clicked', self.on_import_pressed)
        main_layout.attach(btn_import, 4, 2, 1, 1)

        self.btn_delete = Gtk.Button(label='Supprimer')
        self.btn_delete.connect('clicked', self.on_delete_pressed, select)
        self.btn_delete.set_sensitive(False)
        main_layout.attach(self.btn_delete, 4, 5, 1, 1)

        btn_reload = Gtk.Button(label='Rechager')
        btn_reload.connect('clicked', self.update_file_list)
        main_layout.attach(btn_reload, 0, 6, 1, 1)

        btn_help = Gtk.Button(label='Aide')
        btn_help.connect('clicked', self.on_help_pressed)
        main_layout.attach(btn_help, 3, 6, 1, 1)

        btn_quit = Gtk.Button(label='Fermer')
        btn_quit.connect('clicked', self.app_quit)
        main_layout.attach(btn_quit, 4, 6, 1, 1)

        select.connect('changed', self.on_tree_selection_changed)

        self.add(main_layout)

    def update_file_list(self, btn=None):
        self.store.clear()
        planes_path = []

        for plane_file in glob.glob(r'openplane/planes/*.json'):
            planes_path.append(plane_file)

        for plane in planes_path:
                    plane_name = os.path.basename(plane)
                    plane_name = os.path.splitext(plane_name)[0]
                    self.store.append([plane_name, plane])

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            if not self.btn_edit.get_sensitive():
                self.btn_edit.set_sensitive(True)

            if not self.btn_delete.get_sensitive():
                self.btn_delete.set_sensitive(True)
        else:
            self.btn_edit.set_sensitive(False)
            self.btn_delete.set_sensitive(False)

    def on_new_pressed(self, button):
        add_plane = PlanesManagerDialog()
        add_plane.dialog.run()
        self.update_file_list()

    def on_edit_pressed(self, button, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            edit_plane = PlanesManagerDialog(model[treeiter][1])
            edit_plane.dialog.run()
            self.update_file_list()

    def on_import_pressed(self, button):
        dialog = Gtk.FileChooserDialog('Sélectionnez le fichier', self,
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

            shutil.copy(file_path,
                        'openplane/planes/{}.json'.format(plane_name))

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

    def on_delete_pressed(self, button, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            os.remove(model[treeiter][1])
            self.update_file_list()

    def on_help_pressed(self, *args):
        help_window = HelpWindow()
        help_window.connect('delete-event', help_window.app_quit)
        help_window.show_all()

    def app_quit(self, *args):
        self.destroy()

if __name__ == '__main__':
    win = HangarWindow()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
