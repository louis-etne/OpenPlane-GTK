#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

import json


class Plane:

    def __init__(self, values=None):
        if values is not None and len(values) == 64:
            self.create_plane(values)

    def create_plane(self, values):
        # ID section
        self.immatriculation = values[0].upper()
        self.plane_type = values[1].upper()
        self.oaci = values[2].upper()
        self.colors = values[3]

        self.s_croisiere = values[4]
        self.s_montee = values[5]
        self.s_descente = values[6]
        self.v_montee = values[7]
        self.v_descente = values[8]

        self.vso = values[9]
        self.vfe = values[10]
        self.vno = values[11]
        self.vne = values[12]
        self.vx = values[13]
        self.vy = values[14]

        self.carbu_capacity = values[15]
        self.carbu_unit = values[16]
        self.carbu_type = values[17]
        self.carbu_inutilisable = values[18]
        self.carbu_consom = values[19]

        self.piste_dure = values[20]
        self.piste_herbe = values[21]
        self.piste_unit = values[22]

        self.rdba = values[23]
        self.transpondeur = values[24]
        self.turbulance = values[25]
        self.certification = values[26]

        self.equipements = {
            "C": values[27],
            "D": values[28],
            "F": values[29],
            "G": values[30],
            "H": values[31],
            "I": values[32],
            "J": values[33],
            "K": values[34],
            "L": values[35],
            "O": values[36],
            "R": values[37],
            "T": values[38],
            "U": values[39],
            "V": values[40],
            "W": values[41],
            "X": values[42],
            "Y": values[43]
        }

        self.p1x = values[44]
        self.p1y = values[45]
        self.p2x = values[46]
        self.p2y = values[47]
        self.p3x = values[48]
        self.p3y = values[49]
        self.p4x = values[50]
        self.p4y = values[51]
        self.p5x = values[52]
        self.p5y = values[53]

        self.up1x = values[54]
        self.up1y = values[55]
        self.up2x = values[56]
        self.up2y = values[57]
        self.up3x = values[58]
        self.up3y = values[59]
        self.up4x = values[60]
        self.up4y = values[61]
        self.up5x = values[62]
        self.up5y = values[63]

    def save_plane(self):
        filename = 'openplane/planes/{}.json'.format(self.immatriculation)

        plane_values = {
             'Immatriculation': self.immatriculation,
             'Type': self.plane_type,
             'OACI': self.oaci,
             'Couleurs': self.colors,
             'Vitesse': {
                 'Croisiere': self.s_croisiere,
                 'Montee': self.s_montee,
                 'VzMontee': self.v_montee,
                 'Descente': self.s_descente,
                 'VzDescente': self.v_descente,
                 'VSO': self.vso,
                 'VFE': self.vfe,
                 'VNO': self.vno,
                 'VNE': self.vne,
                 'Vx': self.vx,
                 'Vy': self.vy
             },
             'Carburant': {
                 'Type': self.carbu_type,
                 'Capacite': self.carbu_capacity,
                 'Inutilisable': self.carbu_inutilisable,
                 'Consomation': self.carbu_consom,
                 'Unite': self.carbu_unit
             },
             'Piste': {
                 'Dure': self.piste_dure,
                 'Herbe': self.piste_herbe,
                 'Unite': self.piste_unit
             },
             'RDBA': self.rdba,
             'Transpondeur': self.transpondeur,
             'Turbulance': self.turbulance,
             'Certification': self.certification,
             'Equipement': {
                 'C': self.equipements['C'],
                 'D': self.equipements['D'],
                 'F': self.equipements['F'],
                 'G': self.equipements['G'],
                 'H': self.equipements['H'],
                 'I': self.equipements['I'],
                 'J': self.equipements['J'],
                 'K': self.equipements['K'],
                 'L': self.equipements['L'],
                 'O': self.equipements['O'],
                 'R': self.equipements['R'],
                 'T': self.equipements['T'],
                 'U': self.equipements['U'],
                 'V': self.equipements['V'],
                 'W': self.equipements['W'],
                 'X': self.equipements['X'],
                 'Y': self.equipements['Y']
             },
             'Centrage': {
                 'Normale': {
                    'P1x': self.p1x,
                    'P1y': self.p1y,
                    'P2x': self.p2x,
                    'P2y': self.p2y,
                    'P3x': self.p3x,
                    'P3y': self.p3y,
                    'P4x': self.p4x,
                    'P4y': self.p4y,
                    'P5x': self.p5x,
                    'P5y': self.p5y
                 },
                 'Utilitaire': {
                    'P1x': self.up1x,
                    'P1y': self.up1y,
                    'P2x': self.up2x,
                    'P2y': self.up2y,
                    'P3x': self.up3x,
                    'P3y': self.up3y,
                    'P4x': self.up4x,
                    'P4y': self.up4y,
                    'P5x': self.up5x,
                    'P5y': self.up5y
                 }
             }}

        with open(filename, 'w') as outfile:
            json.dump(plane_values, outfile, indent=4)

    def import_plane(self, filepath):
        values = []

        with open(filepath, 'r') as reader:
            datas = json.load(reader)

            values.append(datas['Immatriculation'].upper())
            values.append(datas['Type'].upper())
            values.append(datas['OACI'].upper())
            values.append(datas['Couleurs'])

            values.append(datas['Vitesse']['Croisiere'])
            values.append(datas['Vitesse']['Montee'])
            values.append(datas['Vitesse']['VzMontee'])
            values.append(datas['Vitesse']['Descente'])
            values.append(datas['Vitesse']['VzDescente'])

            values.append(datas['Vitesse']['VSO'])
            values.append(datas['Vitesse']['VFE'])
            values.append(datas['Vitesse']['VNO'])
            values.append(datas['Vitesse']['VNE'])
            values.append(datas['Vitesse']['Vx'])
            values.append(datas['Vitesse']['Vy'])

            values.append(datas['Carburant']['Capacite'])
            values.append(datas['Carburant']['Unite'])
            values.append(datas['Carburant']['Type'])
            values.append(datas['Carburant']['Inutilisable'])
            values.append(datas['Carburant']['Consomation'])

            values.append(datas['Piste']['Dure'])
            values.append(datas['Piste']['Herbe'])
            values.append(datas['Piste']['Unite'])

            values.append(datas['RDBA'])
            values.append(datas['Transpondeur'])
            values.append(datas['Turbulance'])
            values.append(datas['Certification'])

            values.append(datas['Equipement']['C'])
            values.append(datas['Equipement']['D'])
            values.append(datas['Equipement']['F'])
            values.append(datas['Equipement']['G'])
            values.append(datas['Equipement']['H'])
            values.append(datas['Equipement']['I'])
            values.append(datas['Equipement']['J'])
            values.append(datas['Equipement']['K'])
            values.append(datas['Equipement']['L'])
            values.append(datas['Equipement']['O'])
            values.append(datas['Equipement']['R'])
            values.append(datas['Equipement']['T'])
            values.append(datas['Equipement']['U'])
            values.append(datas['Equipement']['V'])
            values.append(datas['Equipement']['W'])
            values.append(datas['Equipement']['X'])
            values.append(datas['Equipement']['Y'])

            values.append(datas['Centrage']['Normale']['P1x'])
            values.append(datas['Centrage']['Normale']['P1y'])
            values.append(datas['Centrage']['Normale']['P2x'])
            values.append(datas['Centrage']['Normale']['P2y'])
            values.append(datas['Centrage']['Normale']['P3x'])
            values.append(datas['Centrage']['Normale']['P3y'])
            values.append(datas['Centrage']['Normale']['P4x'])
            values.append(datas['Centrage']['Normale']['P4y'])
            values.append(datas['Centrage']['Normale']['P5x'])
            values.append(datas['Centrage']['Normale']['P5y'])

            values.append(datas['Centrage']['Utilitaire']['P1x'])
            values.append(datas['Centrage']['Utilitaire']['P1y'])
            values.append(datas['Centrage']['Utilitaire']['P2x'])
            values.append(datas['Centrage']['Utilitaire']['P2y'])
            values.append(datas['Centrage']['Utilitaire']['P3x'])
            values.append(datas['Centrage']['Utilitaire']['P3y'])
            values.append(datas['Centrage']['Utilitaire']['P4x'])
            values.append(datas['Centrage']['Utilitaire']['P4y'])
            values.append(datas['Centrage']['Utilitaire']['P5x'])
            values.append(datas['Centrage']['Utilitaire']['P5y'])

        self.create_plane(values)
