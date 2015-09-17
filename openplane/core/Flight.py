#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from openplane import config
import json


class Flight:

    def __init__(self, values=None):
        if values is not None and len(values) == 20:
            self.create_flight(values)

    def create_flight(self, values):
        self.date = values[0]
        self.plane = values[1]
        self.role = values[2]
        self.type = values[3]

        self.members_day = values[4]
        self.members_night = values[5]

        self.single_engine_day_double = values[6]
        self.single_engine_day_captain = values[7]
        self.single_engine_night_double = values[8]
        self.single_engine_night_captain = values[9]

        self.multi_engines_day_double = values[10]
        self.multi_engines_day_captain = values[11]
        self.multi_engines_day_copilot = values[12]
        self.multi_engines_night_double = values[13]
        self.multi_engines_night_captain = values[14]
        self.multi_engines_night_copilot = values[15]

        self.ifr_double = values[16]
        self.ifr_captain = values[17]

        self.simulation = values[18]
        self.ifr_arrivals = values[19]

    def save_flight(self):
        flight_name = '{}{}{}'.format(config.flightslog_folder, self.date,
                                      config.flights_ext)

        flight_values = {
            'Date': self.date,
            'Plane': self.plane,
            'Role': self.role,
            'Type': self.type,
            'Members': {
                'Day': self.members_day,
                'Night': self.members_night
            },
            'Single_engine': {
                'Day': {
                    'Double': self.single_engine_day_double,
                    'Captain': self.single_engine_day_captain
                },
                'Night': {
                    'Double': self.single_engine_night_double,
                    'Captain': self.single_engine_night_captain
                }
            },
            'Multi_engines': {
                'Day': {
                    'Double': self.multi_engines_day_double,
                    'Captain': self.multi_engines_day_captain,
                    'Co-Pilot': self.multi_engines_day_copilot
                },
                'Night': {
                    'Double': self.multi_engines_night_double,
                    'Captain': self.multi_engines_night_captain,
                    'Co-Pilot': self.multi_engines_night_copilot
                }
            },
            'IFR': {
                'Double': self.ifr_double,
                'Captain': self.ifr_captain
            },
            'Simulation': self.simulation,
            'IFR_arrivals': self.ifr_arrivals
        }

        with open(flight_name, 'w') as outfile:
            json.dump(flight_values, outfile, indent=4, sort_keys=True)

    def import_fligt(self, filepath):
        values = []

        with open(filepath, 'r') as reader:
            datas = json.loads(reader)

            values.append(datas['Date'])
            values.append(datas['Plane'])
            values.append(datas['Role'])
            values.append(datas['Type'])

            values.append(datas['Members']['Day'])
            values.append(datas['Members']['Night'])

            values.append(datas['Single_engine']['Day']['Double'])
            values.append(datas['Single_engine']['Day']['Captain'])
            values.append(datas['Single_engine']['Night']['Double'])
            values.append(datas['Single_engine']['Night']['Captain'])

            values.append(datas['Multi_engines']['Day']['Double'])
            values.append(datas['Multi_engines']['Day']['Captain'])
            values.append(datas['Multi_engines']['Day']['Co-Pilot'])
            values.append(datas['Multi_engines']['Night']['Double'])
            values.append(datas['Multi_engines']['Night']['Captain'])
            values.append(datas['Multi_engines']['Night']['Co-Pilot'])

            values.append(datas['IFR']['Double'])
            values.append(datas['IFR']['Captain'])

            values.append(datas['Simulation'])
            values.append(datas['IFR_arrivals'])

        self.create_flight(values)
