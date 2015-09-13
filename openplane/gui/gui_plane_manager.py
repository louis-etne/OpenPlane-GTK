#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from gi.repository import Gtk
from openplane.gui.gui_help import *
from openplane.core.Plane import *


class PlanesManagerWindow:

    def __init__(self, filepath=None):

        builder = Gtk.Builder()
        builder.add_from_file('openplane/gui/gui_plane_manager.glade')

        handlers = {
            "on_mainWindow_destroy": self.app_quit,
            "on_carbuUnits_changed": self.on_carbuUnits_changed,
            "on_help_clicked": self.on_help_pressed,
            "on_save_clicked": self.on_save_pressed,
            "on_close_clicked": self.app_quit
        }

        builder.connect_signals(handlers)

        self.btn_close = builder.get_object('close')

        self.carbuUnits = builder.get_object('carbuUnits')
        self.uselessCarbuUnits = builder.get_object('uselessCarbuUnits')
        self.consomUnits = builder.get_object('consomUnitsLab')

        preview_centrage = builder.get_object('previewCentrage')
        preview_centrage.set_from_file('openplane/gui/preview_centrage.png')

        # On récupère tous les objets (au nombre de 44)
        self.immatriculation = builder.get_object('immEntry')
        self.plane_type = builder.get_object('typeEntry')
        self.oaci = builder.get_object('oaciEntry')
        self.colors = builder.get_object('colorEntry')

        self.s_croisiere = builder.get_object('sCroisiere')
        self.s_montee = builder.get_object('sMontee')
        self.s_descente = builder.get_object('sDescente')
        self.v_montee = builder.get_object('vMontee')
        self.v_descente = builder.get_object('vDescente')

        self.vso = builder.get_object('vso')
        self.vfe = builder.get_object('vfe')
        self.vno = builder.get_object('vno')
        self.vne = builder.get_object('vne')
        self.vx = builder.get_object('vx')
        self.vy = builder.get_object('vy')

        self.carbu_capacity = builder.get_object('capacity')
        self.carbu_unit = builder.get_object('carbuUnits')
        self.carbu_type = builder.get_object('carbuTypes')
        self.carbu_inutilisable = builder.get_object('inutilisable')
        self.carbu_consom = builder.get_object('consom')

        self.piste_dure = builder.get_object('dureEntry')
        self.piste_herbe = builder.get_object('herbeEntry')
        self.piste_unit = builder.get_object('unitsPiste')

        self.rdba = builder.get_object('rdba')
        self.transpo = builder.get_object('transpondeur')
        self.turbulance = builder.get_object('turbulance')
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

        # Création de la fenêtre principale
        self.window = builder.get_object('mainWindow')

        if filepath is not None:
            self.import_datas_plane(filepath)

    def app_quit(self, *args):
        self.window.destroy()

    def on_help_pressed(self, *args):
        help_window = HelpWindow()
        help_window.connect('delete-event', help_window.app_quit)
        help_window.show_all()

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
        values.append(self.immatriculation.get_text())
        values.append(self.plane_type.get_text())
        values.append(self.oaci.get_text())
        values.append(self.colors.get_text())

        # Section Vitesses
        values.append(int(self.s_montee.get_text()))
        values.append(int(self.s_montee.get_text()))
        values.append(int(self.s_descente.get_text()))
        values.append(int(self.v_montee.get_text()))
        values.append(int(self.v_descente.get_text()))

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
        values.append(int(self.carbu_inutilisable.get_text()))
        values.append(int(self.carbu_consom.get_text()))

        # Section piste
        values.append(int(self.piste_dure.get_text()))
        values.append(int(self.piste_herbe.get_text()))
        values.append(self.piste_unit.get_active_id())

        # Section Caractéristiques
        values.append(self.rdba.get_active_id())
        values.append(self.transpo.get_active_id())
        values.append(self.turbulance.get_active_id())
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

        # Section centrage
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

        plane = Plane()
        plane.create_plane(values)
        plane.save_plane()

        self.app_quit()

    def import_datas_plane(self, filepath):
        plane = Plane()
        plane.import_plane(filepath)

        self.immatriculation.set_text(plane.immatriculation)
        self.plane_type.set_text(plane.plane_type)
        self.oaci.set_text(plane.oaci)
        self.colors.set_text(plane.colors)

        self.s_croisiere.set_text(str(plane.s_croisiere))
        self.s_montee.set_text(str(plane.s_montee))
        self.s_descente.set_text(str(plane.s_descente))
        self.v_montee.set_text(str(plane.v_montee))
        self.v_descente.set_text(str(plane.v_descente))

        self.vso.set_text(str(plane.vso))
        self.vfe.set_text(str(plane.vfe))
        self.vno.set_text(str(plane.vno))
        self.vne.set_text(str(plane.vne))
        self.vx.set_text(str(plane.vx))
        self.vy.set_text(str(plane.vy))

        self.carbu_capacity.set_text(str(plane.carbu_capacity))
        self.carbu_unit.set_active_id(plane.carbu_unit)
        self.carbu_type.set_active_id(plane.carbu_type)
        self.carbu_inutilisable.set_text(str(plane.carbu_inutilisable))
        self.carbu_consom.set_text(str(plane.carbu_consom))

        self.piste_dure.set_text(str(plane.piste_dure))
        self.piste_herbe.set_text(str(plane.piste_herbe))
        self.piste_unit.set_active_id(plane.piste_unit)

        self.rdba.set_active_id(plane.rdba)
        self.transpo.set_active_id(plane.transpondeur)
        self.turbulance.set_active_id(plane.turbulance)
        self.certi.set_active_id(plane.certification)

        self.c.set_active(plane.equipements["C"])
        self.d.set_active(plane.equipements["D"])
        self.f.set_active(plane.equipements["F"])
        self.g.set_active(plane.equipements["G"])
        self.h.set_active(plane.equipements["H"])
        self.i.set_active(plane.equipements["I"])
        self.j.set_active(plane.equipements["J"])
        self.k.set_active(plane.equipements["K"])
        self.l.set_active(plane.equipements["L"])
        self.o.set_active(plane.equipements["O"])
        self.r.set_active(plane.equipements["R"])
        self.t.set_active(plane.equipements["T"])
        self.u.set_active(plane.equipements["U"])
        self.v.set_active(plane.equipements["V"])
        self.w.set_active(plane.equipements["W"])
        self.x.set_active(plane.equipements["X"])
        self.y.set_active(plane.equipements["Y"])

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

        # Ajustements
        self.window.set_title('Modifier {}'.format(plane.immatriculation))
        self.btn_close.set_label('Annuler')
        self.on_carbuUnits_changed()

if __name__ == '__main__':
    win = PlanesManagerWindow('openplane/planes/F-BTBB.json')
    win.window.connect('delete-event', Gtk.main_quit)
    win.window.show_all()
    Gtk.main()
