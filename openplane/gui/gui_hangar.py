#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane.gui.gui_plane_manager import *
from openplane import config
from openplane import text
import shutil
import json
import glob
import os


class HangarDialog():
    def __init__(self, import_=False):
        builder = Gtk.Builder()
        builder.add_from_file(config.hangar)

        handlers = {
            'on_close_clicked': self.app_quit,
            'on_new_clicked': self.on_new_clicked,
            'on_import_clicked': self.on_import_clicked,
            'on_select_changed': self.on_select_changed,
            'on_edit_clicked': self.on_edit_clicked,
            'on_delete_clicked': self.on_delete_clicked
        }

        builder.connect_signals(handlers)

        self.type = import_

        self.select = builder.get_object('planeSelect')

        self.btn_edit = builder.get_object('edit')

        self.btn_delete = builder.get_object('delete')

        if self.type:
            self.btn_ok = builder.get_object('ok')

        self.planes_list = builder.get_object('planesList')
        self.update_file_list()

        self.dialog = builder.get_object('dialog')
        self.dialog.set_icon_from_file(config.logo_path)

    def update_file_list(self, btn=None):
        self.planes_list.clear()
        planes_path = []

        for plane_file in glob.glob('{}*{}'.format(config.planes_folder,
                                                   config.planes_ext)):
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

            if self.type and not self.btn_ok.get_sensitive():
                self.btn_ok.set_sensitive(True)
        else:
            self.btn_edit.set_sensitive(False)
            self.btn_delete.set_sensitive(False)
            if self.type:
                self.btn_ok.set_sensitive(False)

    def on_new_clicked(self, button):
        add_plane = PlanesManagerDialog()
        add_plane.dialog.run()
        self.update_file_list()

    def on_edit_clicked(self, button):
        edit_plane = PlanesManagerDialog(self.return_selected())
        edit_plane.dialog.run()
        self.update_file_list()

    def on_import_clicked(self, button):
        dialog = Gtk.FileChooserDialog(text.select_file, self.dialog,
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

            new_path = '{}{}{}'.format(config.planes_folder, plane_name,
                                       config.planes_ext)

            shutil.copy(file_path, new_path)

            self.update_file_list()
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def get_plane_name(self, filepath):
        with open(filepath, 'r') as reader:
            datas = json.load(reader)

            return datas['Matriculation'].upper()

    def add_filters(self, dialog):
        filter_opp = Gtk.FileFilter()
        filter_opp.set_name(text.opp_files)
        filter_opp.add_pattern('*{}'.format(config.planes_ext))
        dialog.add_filter(filter_opp)

        filter_any = Gtk.FileFilter()
        filter_any.set_name(text.all_files)
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_delete_clicked(self, button):
        os.remove(self.return_selected())
        self.update_file_list()

    def return_selected(self):
        model, treeiter = self.select.get_selected()
        if treeiter is not None:
            return model[treeiter][0]

    def app_quit(self, *args):
        self.dialog.destroy()
