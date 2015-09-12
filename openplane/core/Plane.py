#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

import json


class Plane:

    def __init__(self, values=None):
        if values is not None and len(values) == 44:
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

    def save_plane(self):
        plane_filename = 'openplane/planes/{}.json'.format(self.immatriculation)

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
             }}
        with open(plane_filename, 'w') as outfile:
            json.dump(plane_values, outfile, indent=4)

    def import_plane(self, filepath):
        with open(filepath, 'r') as reader:
            datas = json.load(reader)

            self.immatriculation = datas['Immatriculation'].upper()
            self.plane_type = datas['Type'].upper()
            self.oaci = datas['OACI'].upper()
            self.colors = datas['Couleurs']

            self.s_croisiere = datas['Vitesse']['Croisiere']
            self.s_montee = datas['Vitesse']['Montee']
            self.s_descente = datas['Vitesse']['VzMontee']
            self.v_montee = datas['Vitesse']['Descente']
            self.v_descente = datas['Vitesse']['VzDescente']

            self.vso = datas['Vitesse']['VSO']
            self.vfe = datas['Vitesse']['VFE']
            self.vno = datas['Vitesse']['VNO']
            self.vne = datas['Vitesse']['VNE']
            self.vx = datas['Vitesse']['Vx']
            self.vy = datas['Vitesse']['Vy']

            self.carbu_capacity = datas['Carburant']['Capacite']
            self.carbu_unit = datas['Carburant']['Unite']
            self.carbu_type = datas['Carburant']['Type']
            self.carbu_inutilisable = datas['Carburant']['Inutilisable']
            self.carbu_consom = datas['Carburant']['Consomation']

            self.piste_dure = datas['Piste']['Dure']
            self.piste_herbe = datas['Piste']['Herbe']
            self.piste_unit = datas['Piste']['Unite']

            self.rdba = datas['RDBA']
            self.transpondeur = datas['Transpondeur']
            self.turbulance = datas['Turbulance']
            self.certification = datas['Certification']

            self.equipements = {
                "C": datas['Equipement']['C'],
                "D": datas['Equipement']['D'],
                "F": datas['Equipement']['F'],
                "G": datas['Equipement']['G'],
                "H": datas['Equipement']['H'],
                "I": datas['Equipement']['I'],
                "J": datas['Equipement']['J'],
                "K": datas['Equipement']['K'],
                "L": datas['Equipement']['L'],
                "O": datas['Equipement']['O'],
                "R": datas['Equipement']['R'],
                "T": datas['Equipement']['T'],
                "U": datas['Equipement']['U'],
                "V": datas['Equipement']['V'],
                "W": datas['Equipement']['W'],
                "X": datas['Equipement']['X'],
                "Y": datas['Equipement']['Y']
            }
