#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane import config
from openplane import text
from openplane.core import weather
import json


class AirfieldViewer:
    def __init__(self, code):
        builder = Gtk.Builder()
        builder.add_from_file(config.airfield_viewer)

        handler = {'on_close': self.app_quit}
        builder.connect_signals(handler)

        self.dialog = builder.get_object('dialog')
        self.dialog.set_icon_from_file(config.icon_path)

        self.runways_layout = builder.get_object('runwaysGrid')

        self.name = builder.get_object('name')
        self.code = builder.get_object('code')
        self.geo = builder.get_object('geo')

        self.mag = builder.get_object('magVar')
        self.alt = builder.get_object('alt')
        self.traffic = builder.get_object('traffic')
        self.gund = builder.get_object('gund')
        self.status = builder.get_object('status')

        self.link = builder.get_object('link')

        self.metar = builder.get_object('metar')
        self.taf = builder.get_object('taf')

        airfield = self.get_airfield_datas(code)
        self.set_entry(airfield)
        self.set_weather(airfield)

    def get_airfield_datas(self, code):
        with open(config.airfields, 'r') as input_file:
            airfields = json.load(input_file)

            for airfield in airfields:
                if airfield['Code'] == code:
                    return airfield

    def set_entry(self, airfield):
        self.name.set_text(str(airfield['Name']))
        self.code.set_text(str(airfield['Code']))
        self.geo.set_text(str(airfield['GEO_ARP']))

        self.mag.set_text(str(airfield['MAG']))
        self.alt.set_text(str(airfield['ALT']))
        self.traffic.set_text(str(airfield['Traffic']))
        self.gund.set_text(str(airfield['GUND']))
        self.status.set_text(str(airfield['Status']))

        self.set_runways(airfield)

        link = self.generate_link(str(airfield['Code']).upper())
        self.link.set_markup('<a href="{}">{}</a>'.format(link,
                                                          airfield['Code']))
        self.dialog.set_title('{} - {}'.format(str(airfield['Code']),
                                               str(airfield['Name'])))

    def set_runways(self, airfield):
        i = 0
        for rwy in airfield['Runways']:
            frame = Gtk.Frame()  # Chaque piste à sa frame
            frame.set_label(' - '.join([rwy['Runway_1'], rwy['Runway_2']]))
            frame.set_shadow_type(1)

            # On fait des rangées de 2 frames
            self.runways_layout.attach(frame, (i % 2), int((i / 2)), 1, 1)

            align = Gtk.Alignment.new(0.50, 0.50, 1.00, 1.00)
            align.set_padding(6, 6, 12, 6)
            frame.add(align)

            rwy_layout = Gtk.Grid()
            rwy_layout.set_column_spacing(6)
            rwy_layout.set_column_homogeneous(False)

            rwy_layout.set_row_spacing(6)
            rwy_layout.set_row_homogeneous(False)

            align.add(rwy_layout)

            # Labels
            lab_side1 = Gtk.Label(text.side.format(str(1)))
            rwy_layout.attach(lab_side1, 3, 0, 2, 1)

            lab_side2 = Gtk.Label(text.side.format(str(2)))
            rwy_layout.attach(lab_side2, 6, 0, 2, 1)

            lab_rwy = Gtk.Label(text.rwy)
            rwy_layout.attach(lab_rwy, 2, 1, 1, 1)

            lab_size = Gtk.Label(text.size)
            rwy_layout.attach(lab_size, 2, 2, 1, 1)

            lab_surface = Gtk.Label(text.surface)
            rwy_layout.attach(lab_surface, 2, 3, 1, 1)

            lab_orientation = Gtk.Label(text.orientation)
            rwy_layout.attach(lab_orientation, 2, 4, 1, 1)

            # THR
            lab_thr = Gtk.Label(text.thr)
            rwy_layout.attach(lab_thr, 0, 5, 1, 2)

            thr_sep = Gtk.Separator.new(1)
            rwy_layout.attach(thr_sep, 1, 5, 1, 2)

            lab_thr_position = Gtk.Label(text.position_thr)
            rwy_layout.attach(lab_thr_position, 2, 5, 1, 1)

            lab_thr_alt = Gtk.Label(text.alt_thr)
            rwy_layout.attach(lab_thr_alt, 2, 6, 1, 1)

            # DTHR
            lab_dthr = Gtk.Label(text.dthr)
            rwy_layout.attach(lab_dthr, 0, 7, 1, 2)

            dthr_sep = Gtk.Separator.new(1)
            rwy_layout.attach(dthr_sep, 1, 7, 1, 2)

            lab_dthr_position = Gtk.Label(text.position_dthr)
            rwy_layout.attach(lab_dthr_position, 2, 7, 1, 1)

            lab_dthr_alt = Gtk.Label(text.alt_dthr)
            rwy_layout.attach(lab_dthr_alt, 2, 8, 1, 1)

            lab_status = Gtk.Label(text.status)
            rwy_layout.attach(lab_status, 2, 9, 1, 1)

            # Entries
            entry_rwy1 = Gtk.Entry()
            entry_rwy1.props.editable = False
            entry_rwy1.set_text(str(rwy['Runway_1']))
            rwy_layout.attach(entry_rwy1, 3, 1, 2, 1)

            entry_rwy2 = Gtk.Entry()
            entry_rwy2.props.editable = False
            entry_rwy2.set_text(str(rwy['Runway_2']))
            rwy_layout.attach(entry_rwy2, 6, 1, 2, 1)

            entry_size = Gtk.Entry()
            entry_size.props.editable = False
            entry_size.props.xalign = 0.5
            entry_size.set_text(' x '.join([str(rwy['Length']),
                                            str(rwy['Width'])]))
            rwy_layout.attach(entry_size, 3, 2, 4, 1)

            lab_size_unit = Gtk.Label('m')
            rwy_layout.attach(lab_size_unit, 7, 2, 1, 1)

            entry_surface = Gtk.Entry()
            entry_surface.props.editable = False
            entry_surface.props.xalign = 0.5
            entry_surface.set_text(str(rwy['Surface']))
            rwy_layout.attach(entry_surface, 3, 3, 5, 1)

            entry_geo1 = Gtk.Entry()
            entry_geo1.props.editable = False
            entry_geo1.set_text(str(rwy['Orientation_1']))
            rwy_layout.attach(entry_geo1, 3, 4, 1, 1)

            entry_geo2 = Gtk.Entry()
            entry_geo2.props.editable = False
            entry_geo2.set_text(str(rwy['Orientation_2']))
            rwy_layout.attach(entry_geo2, 6, 4, 1, 1)

            label_geo1_unit = Gtk.Label('°')
            rwy_layout.attach(label_geo1_unit, 4, 4, 1, 1)

            label_geo2_unit = Gtk.Label('°')
            rwy_layout.attach(label_geo2_unit, 7, 4, 1, 1)

            thr_pos1 = Gtk.Entry()
            thr_pos1.props.editable = False
            thr_pos1.set_text(str(rwy['THR_position_1']))
            rwy_layout.attach(thr_pos1, 3, 5, 1, 1)

            thr_pos2 = Gtk.Entry()
            thr_pos2.props.editable = False
            thr_pos2.set_text(str(rwy['THR_position_2']))
            rwy_layout.attach(thr_pos2, 6, 5, 1, 1)

            thr_alt1 = Gtk.Entry()
            thr_alt1.props.editable = False
            thr_alt1.set_text(str(rwy['THR_alt_1']))
            rwy_layout.attach(thr_alt1, 3, 6, 1, 1)

            thr_alt2 = Gtk.Entry()
            thr_alt2.props.editable = False
            thr_alt2.set_text(str(rwy['THR_alt_2']))
            rwy_layout.attach(thr_alt2, 6, 6, 1, 1)

            label_thr_alt1 = Gtk.Label('ft')
            rwy_layout.attach(label_thr_alt1, 4, 6, 1, 1)

            label_thr_alt2 = Gtk.Label('ft')
            rwy_layout.attach(label_thr_alt2, 7, 6, 1, 1)

            dthr_pos1 = Gtk.Entry()
            dthr_pos1.props.editable = False
            dthr_pos1.set_text(str(rwy['DTHR_position_1']))
            rwy_layout.attach(dthr_pos1, 3, 7, 1, 1)

            dthr_pos2 = Gtk.Entry()
            dthr_pos2.props.editable = False
            dthr_pos2.set_text(str(rwy['DTHR_position_2']))
            rwy_layout.attach(dthr_pos2, 6, 7, 1, 1)

            dthr_alt1 = Gtk.Entry()
            dthr_alt1.props.editable = False
            dthr_alt1.set_text(str(rwy['DTHR_alt_1']))
            rwy_layout.attach(dthr_alt1, 3, 8, 1, 1)

            dthr_alt2 = Gtk.Entry()
            dthr_alt2.props.editable = False
            dthr_alt2.set_text(str(rwy['DTHR_alt_2']))
            rwy_layout.attach(dthr_alt2, 6, 8, 1, 1)

            label_dthr_alt1 = Gtk.Label('ft')
            rwy_layout.attach(label_dthr_alt1, 4, 8, 1, 1)

            label_dthr_alt2 = Gtk.Label('ft')
            rwy_layout.attach(label_dthr_alt2, 7, 8, 1, 1)

            entry_status = Gtk.Entry()
            entry_status.props.editable = False
            entry_status.set_text(str(rwy['Status']))
            rwy_layout.attach(entry_status, 3, 9, 5, 1)

            # Separators
            sep1 = Gtk.Separator.new(1)
            rwy_layout.attach(sep1, 5, 0, 1, 2)

            sep2 = Gtk.Separator.new(1)
            rwy_layout.attach(sep2, 5, 4, 1, 5)

            i += 1

        dialog_width, dialog_height = self.dialog.get_size()
        add_width = 25
        add_height = 190
        if i == 1:
            self.dialog.resize(dialog_width + add_width,
                               dialog_height + add_height)
        else:
            self.dialog.resize((dialog_width*2) + add_width,
                               dialog_height + add_height)

        self.runways_layout.show_all()

    def generate_link(self, code):
        link = 'https://www.sia.aviation-civile.gouv.fr/aip/enligne/' \
               'Atlas-VAC/PDF_AIPparSSection/VAC/AD/2/1511_AD-2.{}.pdf'

        return link.format(code)


    def set_weather(self, airfield):
        metar = weather.get_metar(str(airfield['Code']))
        taf = weather.get_taf(str(airfield['Code']))
        if metar is None:
            self.metar.set_label('Impossible de télécharger le METAR. Deux raisons possibles :\n'
                               '\t- Le terrain choisis ne possède pas de METAR associé.\n'
                               '\t- La connexion avec le serveur n\'est pas possible.')
        else:
            self.metar.set_label(metar)

        if taf is None:
            self.taf.set_label('Impossible de télécharger le TAF. Deux raisons possibles :\n'
                               '\t- Le terrain choisis ne possède pas de TAF associé.\n'
                               '\t- La connexion avec le serveur n\'est pas possible.')
        else:
            self.taf.set_label(taf)

    def app_quit(self, button):
        self.dialog.destroy()
