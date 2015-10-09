#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne


from gi.repository import Gtk
from openplane.gui.gui_airfield_viewer import *
from openplane import config
import json


class AirfieldSelectorDialog:

    def __init__(self, local=False):
        builder = Gtk.Builder()
        builder.add_from_file(config.airfields_selector)

        handler = {
           'on_close': self.app_quit,
           'on_search_options_changed': self.on_search_options_changed,
           'on_search_changed': self.on_search_changed,
           'on_select_changed': self.on_select_changed,
           'on_open': self.on_open
        }
        builder.connect_signals(handler)

        self.airfields_list = builder.get_object('airfieldsList')

        with open(config.airfields, 'r') as data_file:
            data = json.load(data_file)

            for airfield in data:
                self.airfields_list.append([airfield['Code'],
                                            airfield['Name']])

        if local == True:
            self.airfields_list.append(['HOME', 'Vol locale'])

        self.scroll_box = builder.get_object('scrollBox')
        self.tree_view = builder.get_object('airfieldsView')

        self.radio_code_search = builder.get_object('searchCode')
        self.search_entry = builder.get_object('search')
        self.completion = builder.get_object('completion')

        self.selector = builder.get_object('airfieldSelect')

        # On récupère les boutons
        self.open = builder.get_object('open')
        self.ok = builder.get_object('ok')

        self.dialog = builder.get_object('dialog')
        self.dialog.set_icon_from_file(config.icon_path)

    def on_search_options_changed(self, radio):
        if self.radio_code_search.get_active():
            self.search_entry.set_text('')
            self.completion.props.text_column = 0
            self.search_entry.set_max_length(4)
        else:
            self.search_entry.set_text('')
            self.completion.props.text_column = 1
            self.search_entry.set_max_length(100)

    def on_search_changed(self, entry):
        text = self.search_entry.get_text()

        if self.radio_code_search.get_active():
            if len(text) == 4:
                count = 0

                for airfield in self.airfields_list:
                    if text == airfield[0]:
                        break
                    count += 1
                if count < len(self.airfields_list):
                    tree_iter = self.airfields_list.get_iter(count)
                    self.selector.select_iter(tree_iter)
                # On place correctement les ascenseurs
                adj = self.tree_view.get_vadjustment()
                adj.set_value(adj.get_lower() + count * 23)
        else:
            count = 0

            for airfield in self.airfields_list:
                if text == airfield[1]:
                    break
                count += 1
            if count < len(self.airfields_list):
                self.selector.select_iter(self.airfields_list.get_iter(count))
                # On place correctement les ascenseurs
                adj = self.tree_view.get_vadjustment()
                adj.set_value(adj.get_lower() + count * 23)

    def on_select_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            if not self.open.get_sensitive():
                self.open.set_sensitive(True)

            if not self.ok.get_sensitive():
                self.ok.set_sensitive(True)
        else:
            self.open.set_sensitive(False)
            self.ok.set_sensitive(False)

    def on_open(self, button, *args):
        model, treeiter = self.selector.get_selected()
        if treeiter is not None:
            airfield_viewer = AirfieldViewer(model[treeiter][0])
            airfield_viewer.dialog.run()

    def return_airfield(self):
        model, treeiter = self.selector.get_selected()
        if treeiter is not None:
            return model[treeiter][0]

    def app_quit(self, button):
        self.dialog.destroy()
