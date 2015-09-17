#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from openplane import config
import json


class Plane:

    def __init__(self, values=None):
        if values is not None and len(values) == 73:
            self.create_plane(values)

    def create_plane(self, values):
        # ID section
        self.matriculation = values[0].upper()
        self.plane_type = values[1].upper()
        self.oaci = values[2].upper()
        self.colors = values[3]

        self.s_cruising = values[4]
        self.s_up = values[5]
        self.s_low = values[6]
        self.v_up = values[7]
        self.v_low = values[8]

        self.vso = values[9]
        self.vfe = values[10]
        self.vno = values[11]
        self.vne = values[12]
        self.vx = values[13]
        self.vy = values[14]

        self.carbu_capacity = values[15]
        self.carbu_unit = values[16]
        self.carbu_type = values[17]
        self.carbu_useless = values[18]
        self.carbu_consom = values[19]

        self.runway_hard = values[20]
        self.runway_grass = values[21]
        self.runway_unit = values[22]

        self.rdba = values[23]
        self.transponder = values[24]
        self.turbulence = values[25]
        self.certification = values[26]

        self.equipments = {
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

        self.utility = values[64]

        self.empty_mass = values[65]
        self.empty_bdl = values[66]
        self.options_mass = values[67]
        self.options_bdl = values[68]
        self.pass_av = values[69]
        self.pass_ar = values[70]
        self.fuel = values[71]
        self.baggage = values[72]

    def save_plane(self):
        filename = '{}{}{}'.format(config.planes_folder, self.matriculation,
                                   config.planes_ext)

        plane_values = {
             'Matriculation': self.matriculation,
             'Type': self.plane_type,
             'OACI': self.oaci,
             'Colors': self.colors,
             'Speeds': {
                 'Crusing': self.s_cruising,
                 'Climb': self.s_up,
                 'VzClimb': self.v_up,
                 'Descent': self.s_low,
                 'VzDescent': self.v_low,
                 'VSO': self.vso,
                 'VFE': self.vfe,
                 'VNO': self.vno,
                 'VNE': self.vne,
                 'Vx': self.vx,
                 'Vy': self.vy
             },
             'Fuel': {
                 'Type': self.carbu_type,
                 'Capacity': self.carbu_capacity,
                 'Unusable': self.carbu_useless,
                 'Consumption': self.carbu_consom,
                 'Unit': self.carbu_unit
             },
             'Runway': {
                 'Hard': self.runway_hard,
                 'Grass': self.runway_grass,
                 'Unit': self.runway_unit
             },
             'RDBA': self.rdba,
             'Transponder': self.transponder,
             'Turbulance': self.turbulence,
             'Certification': self.certification,
             'Equipments': {
                 'C': self.equipments['C'],
                 'D': self.equipments['D'],
                 'F': self.equipments['F'],
                 'G': self.equipments['G'],
                 'H': self.equipments['H'],
                 'I': self.equipments['I'],
                 'J': self.equipments['J'],
                 'K': self.equipments['K'],
                 'L': self.equipments['L'],
                 'O': self.equipments['O'],
                 'R': self.equipments['R'],
                 'T': self.equipments['T'],
                 'U': self.equipments['U'],
                 'V': self.equipments['V'],
                 'W': self.equipments['W'],
                 'X': self.equipments['X'],
                 'Y': self.equipments['Y']
             },
             'Balance': {
                 'Normal': {
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
                 'Utility': {
                    'P1x': self.up1x,
                    'P1y': self.up1y,
                    'P2x': self.up2x,
                    'P2y': self.up2y,
                    'P3x': self.up3x,
                    'P3y': self.up3y,
                    'P4x': self.up4x,
                    'P4y': self.up4y,
                    'P5x': self.up5x,
                    'P5y': self.up5y,
                    'Show': self.utility
                 },
                 'Empty_mass': {
                    'Mass': self.empty_mass,
                    'Lever_arm': self.empty_bdl
                 },
                 'Options': {
                    'Mass': self.options_mass,
                    'Lever_arm': self.options_bdl
                 },
                 'Pax_AV': {
                    'Lever_arm': self.pass_av
                 },
                 'Pax_AR': {
                    'Lever_arm': self.pass_ar
                 },
                 'Fuel': {
                    'Lever_arm': self.fuel
                 },
                 'Baggage': {
                    'Lever_arm': self.baggage
                 }
             }}

        with open(filename, 'w') as outfile:
            json.dump(plane_values, outfile, indent=4, sort_keys=True)

    def import_plane(self, filepath):
        values = []

        with open(filepath, 'r') as reader:
            datas = json.load(reader)

            values.append(datas['Matriculation'].upper())
            values.append(datas['Type'].upper())
            values.append(datas['OACI'].upper())
            values.append(datas['Colors'])

            values.append(datas['Speeds']['Crusing'])
            values.append(datas['Speeds']['Climb'])
            values.append(datas['Speeds']['VzClimb'])
            values.append(datas['Speeds']['Descent'])
            values.append(datas['Speeds']['VzDescent'])

            values.append(datas['Speeds']['VSO'])
            values.append(datas['Speeds']['VFE'])
            values.append(datas['Speeds']['VNO'])
            values.append(datas['Speeds']['VNE'])
            values.append(datas['Speeds']['Vx'])
            values.append(datas['Speeds']['Vy'])

            values.append(datas['Fuel']['Capacity'])
            values.append(datas['Fuel']['Unit'])
            values.append(datas['Fuel']['Type'])
            values.append(datas['Fuel']['Unusable'])
            values.append(datas['Fuel']['Consumption'])

            values.append(datas['Runway']['Hard'])
            values.append(datas['Runway']['Grass'])
            values.append(datas['Runway']['Unit'])

            values.append(datas['RDBA'])
            values.append(datas['Transponder'])
            values.append(datas['Turbulance'])
            values.append(datas['Certification'])

            values.append(datas['Equipments']['C'])
            values.append(datas['Equipments']['D'])
            values.append(datas['Equipments']['F'])
            values.append(datas['Equipments']['G'])
            values.append(datas['Equipments']['H'])
            values.append(datas['Equipments']['I'])
            values.append(datas['Equipments']['J'])
            values.append(datas['Equipments']['K'])
            values.append(datas['Equipments']['L'])
            values.append(datas['Equipments']['O'])
            values.append(datas['Equipments']['R'])
            values.append(datas['Equipments']['T'])
            values.append(datas['Equipments']['U'])
            values.append(datas['Equipments']['V'])
            values.append(datas['Equipments']['W'])
            values.append(datas['Equipments']['X'])
            values.append(datas['Equipments']['Y'])

            values.append(datas['Balance']['Normal']['P1x'])
            values.append(datas['Balance']['Normal']['P1y'])
            values.append(datas['Balance']['Normal']['P2x'])
            values.append(datas['Balance']['Normal']['P2y'])
            values.append(datas['Balance']['Normal']['P3x'])
            values.append(datas['Balance']['Normal']['P3y'])
            values.append(datas['Balance']['Normal']['P4x'])
            values.append(datas['Balance']['Normal']['P4y'])
            values.append(datas['Balance']['Normal']['P5x'])
            values.append(datas['Balance']['Normal']['P5y'])

            values.append(datas['Balance']['Utility']['P1x'])
            values.append(datas['Balance']['Utility']['P1y'])
            values.append(datas['Balance']['Utility']['P2x'])
            values.append(datas['Balance']['Utility']['P2y'])
            values.append(datas['Balance']['Utility']['P3x'])
            values.append(datas['Balance']['Utility']['P3y'])
            values.append(datas['Balance']['Utility']['P4x'])
            values.append(datas['Balance']['Utility']['P4y'])
            values.append(datas['Balance']['Utility']['P5x'])
            values.append(datas['Balance']['Utility']['P5y'])

            values.append(datas['Balance']['Utility']['Show'])

            values.append(datas['Balance']['Empty_mass']['Mass'])
            values.append(datas['Balance']['Empty_mass']['Lever_arm'])
            values.append(datas['Balance']['Options']['Mass'])
            values.append(datas['Balance']['Options']['Lever_arm'])
            values.append(datas['Balance']['Pax_AV']['Lever_arm'])
            values.append(datas['Balance']['Pax_AR']['Lever_arm'])
            values.append(datas['Balance']['Fuel']['Lever_arm'])
            values.append(datas['Balance']['Baggage']['Lever_arm'])

        self.create_plane(values)
