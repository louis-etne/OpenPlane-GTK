#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane.core.Plane import *
from openplane import config
from openplane import text


class PlanesManagerDialog:

    def __init__(self, filepath=None):

        builder = Gtk.Builder()
        builder.add_from_file(config.plane_manager)

        handlers = {
            "on_carbuUnits_changed": self.on_carbuUnits_changed,
            "on_showUtil_toggled": self.on_showUtil_toggled,
            "on_save_clicked": self.on_save_pressed,
            "on_spin_changed": self.on_spin_changed,
            "on_close_clicked": self.app_quit
        }

        builder.connect_signals(handlers)

        self.btn_close = builder.get_object('close')

        self.carbuUnits = builder.get_object('carbuUnits')
        self.uselessCarbuUnits = builder.get_object('uselessCarbuUnits')
        self.consomUnits = builder.get_object('consomUnitsLab')

        preview_balance = builder.get_object('previewCentrage')
        preview_balance.set_from_file(config.preview_balance)

        # On récupère tous les objets (au nombre de 44)
        self.matriculation = builder.get_object('immEntry')
        self.plane_type = builder.get_object('typeEntry')
        self.oaci = builder.get_object('oaciEntry')
        self.colors = builder.get_object('colorEntry')

        self.s_cruising = builder.get_object('sCroisiere')
        self.s_up = builder.get_object('sMontee')
        self.s_low = builder.get_object('sDescente')
        self.v_up = builder.get_object('vMontee')
        self.v_low = builder.get_object('vDescente')

        self.vso = builder.get_object('vso')
        self.vfe = builder.get_object('vfe')
        self.vno = builder.get_object('vno')
        self.vne = builder.get_object('vne')
        self.vx = builder.get_object('vx')
        self.vy = builder.get_object('vy')

        self.carbu_capacity = builder.get_object('capacity')
        self.carbu_unit = builder.get_object('carbuUnits')
        self.carbu_type = builder.get_object('carbuTypes')
        self.carbu_useless = builder.get_object('inutilisable')
        self.carbu_consom = builder.get_object('consom')

        self.runway_hard = builder.get_object('dureEntry')
        self.runway_grass = builder.get_object('herbeEntry')
        self.runway_unit = builder.get_object('unitsPiste')

        self.rdba = builder.get_object('rdba')
        self.transpo = builder.get_object('transpondeur')
        self.turbulence = builder.get_object('turbulence')
        self.certi = builder.get_object('certification')

        self.c = builder.get_object('c')
        self.d = builder.get_object('d')
        self.f = builder.get_object('f')
        self.g = builder.get_object('g')
        self.h = builder.get_object('h')
        self.i = builder.get_object('i')
        self.j = builder.get_object('j')
        self.k = builder.get_object('k')
        self.l = builder.get_object('l')
        self.o = builder.get_object('o')
        self.r = builder.get_object('r')
        self.t = builder.get_object('t')
        self.u = builder.get_object('u')
        self.v = builder.get_object('v')
        self.w = builder.get_object('w')
        self.x = builder.get_object('x')
        self.y = builder.get_object('y')

        self.p1x = builder.get_object('p1x')
        self.p1y = builder.get_object('p1y')
        self.p2x = builder.get_object('p2x')
        self.p2y = builder.get_object('p2y')
        self.p3x = builder.get_object('p3x')
        self.p3y = builder.get_object('p3y')
        self.p4x = builder.get_object('p4x')
        self.p4y = builder.get_object('p4y')
        self.p5x = builder.get_object('p5x')
        self.p5y = builder.get_object('p5y')

        self.up1x = builder.get_object('up1x')
        self.up1y = builder.get_object('up1y')
        self.up2x = builder.get_object('up2x')
        self.up2y = builder.get_object('up2y')
        self.up3x = builder.get_object('up3x')
        self.up3y = builder.get_object('up3y')
        self.up4x = builder.get_object('up4x')
        self.up4y = builder.get_object('up4y')
        self.up5x = builder.get_object('up5x')
        self.up5y = builder.get_object('up5y')

        self.show_utility = builder.get_object('showUtil')

        self.empty_mass = builder.get_object('masseVideStd1')
        self.empty_bdl = builder.get_object('masseVideStd2')
        self.options_mass = builder.get_object('options1')
        self.options_bdl = builder.get_object('options2')
        self.pass_av = builder.get_object('passagersAv2')
        self.pass_ar = builder.get_object('passagersAr2')
        self.carbu = builder.get_object('carbu2')
        self.bagages = builder.get_object('bagages2')

        self.total_empty = builder.get_object('masseVideStd')
        self.total_options = builder.get_object('options')
        self.total_mass = builder.get_object('masseVideBase1')
        self.total_bdl = builder.get_object('bdlMasseVide')
        self.total_total = builder.get_object('masseVideBase2')

        # Création de la fenêtre principale
        self.dialog = builder.get_object('dialog')
        self.dialog.set_icon_from_file(config.icon_path)

        if filepath is not None:
            self.import_datas_plane(filepath)

    def app_quit(self, *args):
        self.dialog.destroy()

    def on_spin_changed(self, spin):
        self.calc_label()

    def calc_label(self):
        empty_moment = self.empty_mass.get_value() * self.empty_bdl.get_value()
        options_moment = self.options_mass.get_value() * self.options_bdl.get_value()
        total1 = self.empty_mass.get_value() + self.options_mass.get_value()
        total2 = self.empty_bdl.get_value() + self.options_bdl.get_value()
        total_moment = empty_moment + options_moment

        self.total_empty.set_text(str(round(empty_moment, 3)))
        self.total_options.set_text(str(round(options_moment, 3)))
        self.total_mass.set_text(str(round(total1, 3)))
        self.total_bdl.set_text(str(round(total2, 3)))
        self.total_total.set_text(str(round(total_moment, 3)))

    def on_showUtil_toggled(self, box):
        if box.get_active():
            self.up1x.set_editable(True)
            self.up1y.set_editable(True)
            self.up2x.set_editable(True)
            self.up2y.set_editable(True)
            self.up3x.set_editable(True)
            self.up3y.set_editable(True)
            self.up4x.set_editable(True)
            self.up4y.set_editable(True)
            self.up5x.set_editable(True)
            self.up5y.set_editable(True)
        else:
            self.up1x.set_editable(False)
            self.up1y.set_editable(False)
            self.up2x.set_editable(False)
            self.up2y.set_editable(False)
            self.up3x.set_editable(False)
            self.up3y.set_editable(False)
            self.up4x.set_editable(False)
            self.up4y.set_editable(False)
            self.up5x.set_editable(False)
            self.up5y.set_editable(False)

    def on_carbuUnits_changed(self, *args):
        units = self.carbuUnits.get_active()
        if units == 0:
            self.uselessCarbuUnits.set_text('L')
            self.consomUnits.set_text('L/h')
        elif units == 1:
            self.uselessCarbuUnits.set_text('Gal')
            self.consomUnits.set_text('Gal/h')
        elif units == 2:
            self.uselessCarbuUnits.set_text('kg')
            self.consomUnits.set_text('kg/h')
        elif units == 3:
            self.uselessCarbuUnits.set_text('lbs')
            self.consomUnits.set_text('lbs/h')
        else:
            self.uselessCarbuUnits.set_text('L')
            self.consomUnits.set_text('L/h')

    def on_save_pressed(self, *args):
        values = []

        # tous les widgets contenant des valeurs à enregistrer
        # Section id
        values.append(self.matriculation.get_text())
        values.append(self.plane_type.get_text())
        values.append(self.oaci.get_text())
        values.append(self.colors.get_text())

        # Section Vitesses
        values.append(int(self.s_cruising.get_text()))
        values.append(int(self.s_up.get_text()))
        values.append(int(self.s_low.get_text()))
        values.append(int(self.v_up.get_text()))
        values.append(int(self.v_low.get_text()))

        values.append(int(self.vso.get_text()))
        values.append(int(self.vfe.get_text()))
        values.append(int(self.vno.get_text()))
        values.append(int(self.vne.get_text()))
        values.append(int(self.vx.get_text()))
        values.append(int(self.vy.get_text()))

        # Section carburant
        values.append(int(self.carbu_capacity.get_text()))
        values.append(self.carbu_unit.get_active_id())
        values.append(self.carbu_type.get_active_id())
        values.append(int(self.carbu_useless.get_text()))
        values.append(int(self.carbu_consom.get_text()))

        # Section piste
        values.append(int(self.runway_hard.get_text()))
        values.append(int(self.runway_grass.get_text()))
        values.append(self.runway_unit.get_active_id())

        # Section Caractéristiques
        values.append(self.rdba.get_active_id())
        values.append(self.transpo.get_active_id())
        values.append(self.turbulence.get_active_id())
        values.append(self.certi.get_active_id())

        # Section Équipements
        values.append(self.c.get_active())
        values.append(self.d.get_active())
        values.append(self.f.get_active())
        values.append(self.g.get_active())
        values.append(self.h.get_active())
        values.append(self.i.get_active())
        values.append(self.j.get_active())
        values.append(self.k.get_active())
        values.append(self.l.get_active())
        values.append(self.o.get_active())
        values.append(self.r.get_active())
        values.append(self.t.get_active())
        values.append(self.u.get_active())
        values.append(self.v.get_active())
        values.append(self.w.get_active())
        values.append(self.x.get_active())
        values.append(self.y.get_active())

        # Section centering
        values.append(float(self.p1x.get_text()))
        values.append(float(self.p1y.get_text()))
        values.append(float(self.p2x.get_text()))
        values.append(float(self.p2y.get_text()))
        values.append(float(self.p3x.get_text()))
        values.append(float(self.p3y.get_text()))
        values.append(float(self.p4x.get_text()))
        values.append(float(self.p4y.get_text()))
        values.append(float(self.p5x.get_text()))
        values.append(float(self.p5y.get_text()))

        values.append(float(self.up1x.get_text()))
        values.append(float(self.up1y.get_text()))
        values.append(float(self.up2x.get_text()))
        values.append(float(self.up2y.get_text()))
        values.append(float(self.up3x.get_text()))
        values.append(float(self.up3y.get_text()))
        values.append(float(self.up4x.get_text()))
        values.append(float(self.up4y.get_text()))
        values.append(float(self.up5x.get_text()))
        values.append(float(self.up5y.get_text()))

        values.append(self.show_utility.get_active())

        values.append(float(self.empty_mass.get_text()))
        values.append(float(self.empty_bdl.get_text()))
        values.append(float(self.options_mass.get_text()))
        values.append(float(self.options_bdl.get_text()))
        values.append(float(self.pass_av.get_text()))
        values.append(float(self.pass_ar.get_text()))
        values.append(float(self.carbu.get_text()))
        values.append(float(self.bagages.get_text()))

        plane = Plane()
        plane.create_plane(values)
        plane.save_plane()

        self.app_quit()

    def import_datas_plane(self, filepath):
        plane = Plane()
        plane.import_plane(filepath)

        self.matriculation.set_text(plane.matriculation)
        self.plane_type.set_text(plane.plane_type)
        self.oaci.set_text(plane.oaci)
        self.colors.set_text(plane.colors)

        self.s_cruising.set_text(str(plane.s_cruising))
        self.s_up.set_text(str(plane.s_up))
        self.s_low.set_text(str(plane.s_low))
        self.v_up.set_text(str(plane.v_up))
        self.v_low.set_text(str(plane.v_low))

        self.vso.set_text(str(plane.vso))
        self.vfe.set_text(str(plane.vfe))
        self.vno.set_text(str(plane.vno))
        self.vne.set_text(str(plane.vne))
        self.vx.set_text(str(plane.vx))
        self.vy.set_text(str(plane.vy))

        self.carbu_capacity.set_text(str(plane.carbu_capacity))
        self.carbu_unit.set_active_id(plane.carbu_unit)
        self.carbu_type.set_active_id(plane.carbu_type)
        self.carbu_useless.set_text(str(plane.carbu_useless))
        self.carbu_consom.set_text(str(plane.carbu_consom))

        self.runway_hard.set_text(str(plane.runway_hard))
        self.runway_grass.set_text(str(plane.runway_grass))
        self.runway_unit.set_active_id(plane.runway_unit)

        self.rdba.set_active_id(plane.rdba)
        self.transpo.set_active_id(plane.transponder)
        self.turbulence.set_active_id(plane.turbulence)
        self.certi.set_active_id(plane.certification)

        self.c.set_active(plane.equipments["C"])
        self.d.set_active(plane.equipments["D"])
        self.f.set_active(plane.equipments["F"])
        self.g.set_active(plane.equipments["G"])
        self.h.set_active(plane.equipments["H"])
        self.i.set_active(plane.equipments["I"])
        self.j.set_active(plane.equipments["J"])
        self.k.set_active(plane.equipments["K"])
        self.l.set_active(plane.equipments["L"])
        self.o.set_active(plane.equipments["O"])
        self.r.set_active(plane.equipments["R"])
        self.t.set_active(plane.equipments["T"])
        self.u.set_active(plane.equipments["U"])
        self.v.set_active(plane.equipments["V"])
        self.w.set_active(plane.equipments["W"])
        self.x.set_active(plane.equipments["X"])
        self.y.set_active(plane.equipments["Y"])

        self.p1x.set_text(str(plane.p1x))
        self.p1y.set_text(str(plane.p1y))
        self.p2x.set_text(str(plane.p2x))
        self.p2y.set_text(str(plane.p2y))
        self.p3x.set_text(str(plane.p3x))
        self.p3y.set_text(str(plane.p3y))
        self.p4x.set_text(str(plane.p4x))
        self.p4y.set_text(str(plane.p4y))
        self.p5x.set_text(str(plane.p5x))
        self.p5y.set_text(str(plane.p5y))

        self.up1x.set_text(str(plane.up1x))
        self.up1y.set_text(str(plane.up1y))
        self.up2x.set_text(str(plane.up2x))
        self.up2y.set_text(str(plane.up2y))
        self.up3x.set_text(str(plane.up3x))
        self.up3y.set_text(str(plane.up3y))
        self.up4x.set_text(str(plane.up4x))
        self.up4y.set_text(str(plane.up4y))
        self.up5x.set_text(str(plane.up5x))
        self.up5y.set_text(str(plane.up5y))

        self.show_utility.set_active(plane.utility)

        self.empty_mass.set_value(plane.empty_mass)
        self.empty_bdl.set_value(plane.empty_bdl)
        self.options_mass.set_value(plane.options_mass)
        self.options_bdl.set_value(plane.options_bdl)
        self.pass_av.set_value(plane.pass_av)
        self.pass_ar.set_value(plane.pass_ar)
        self.carbu.set_value(plane.fuel)
        self.bagages.set_value(plane.baggage)

        # Ajustements
        self.calc_label()
        self.dialog.set_title(text.edit_plane.format(plane.matriculation))
        self.on_carbuUnits_changed()
