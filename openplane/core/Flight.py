#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from openplane import config
from datetime import timedelta
import json


class Flight:

    def __init__(self, values=None):
        if values is not None and len(values) == 28:
            self.create_flight(values)

    def create_flight(self, values):
        self.date = values[0]
        self.plane = values[1]
        self.role = values[2]
        self.type = values[3]

        self.members_day = values[4]
        self.members_hours = values[5]
        self.members_minutes = values[6]

        self.single_engine_day = values[7]
        self.single_engine_double = values[8]
        self.single_engine_hours = values[9]
        self.single_engine_minutes = values[10]

        self.multi_engines_day = values[11]
        self.multi_engines_double = values[12]
        self.multi_engines_captain = values[13]
        self.multi_engines_hours = values[14]
        self.multi_engines_minutes = values[15]

        self.ifr_double = values[16]
        self.ifr_hours = values[17]
        self.ifr_minutes = values[18]

        self.simulation_hours = values[19]
        self.simulation_minutes = values[20]
        self.ifr_arrivals = values[21]

        self.observations = values[22]

        self.takeoff = values[23]
        self.landing = values[24]
        self.departure = values[25]
        self.arrival = values[26]
        self.comments = values[27]

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
                'Hours': self.members_hours,
                'Minutes': self.members_minutes
            },
            'Single_engine': {
                'Day': self.single_engine_day,
                'Double': self.single_engine_double,
                'Hours': self.single_engine_hours,
                'Minutes': self.single_engine_minutes
            },
            'Multi_engines': {
                'Day': self.multi_engines_day,
                'Double': self.multi_engines_double,
                'Captain': self.multi_engines_captain,
                'Hours': self.multi_engines_hours,
                'Minutes': self.multi_engines_minutes
            },
            'IFR': {
                'Double': self.ifr_double,
                'Hours': self.ifr_hours,
                'Minutes': self.ifr_minutes,
                'Arrivals': self.ifr_arrivals,
            },
            'Simulation': {
                'Hours': self.simulation_hours,
                'Minutes': self.simulation_minutes
            },

            'Observations': self.observations,
            'Take-off': self.takeoff,
            'Landing': self.landing,
            'Airfields': {
                'Departure': self.departure,
                'Arrival': self.arrival
            },
            'Comments': self.comments
        }

        with open(flight_name, 'w') as outfile:
            json.dump(flight_values, outfile, indent=4, sort_keys=True)

    def import_flight(self, filepath):
        values = []

        with open(filepath, 'r') as reader:
            datas = json.load(reader)

            values.append(datas['Date'])
            values.append(datas['Plane'])
            values.append(datas['Role'])
            values.append(datas['Type'])

            values.append(datas['Members']['Day'])
            values.append(datas['Members']['Hours'])
            values.append(datas['Members']['Minutes'])

            values.append(datas['Single_engine']['Day'])
            values.append(datas['Single_engine']['Double'])
            values.append(datas['Single_engine']['Hours'])
            values.append(datas['Single_engine']['Minutes'])

            values.append(datas['Multi_engines']['Day'])
            values.append(datas['Multi_engines']['Double'])
            values.append(datas['Multi_engines']['Captain'])
            values.append(datas['Multi_engines']['Hours'])
            values.append(datas['Multi_engines']['Minutes'])

            values.append(datas['IFR']['Double'])
            values.append(datas['IFR']['Hours'])
            values.append(datas['IFR']['Minutes'])

            values.append(datas['Simulation']['Hours'])
            values.append(datas['Simulation']['Minutes'])

            values.append(datas['IFR']['Arrivals'])

            values.append(datas['Observations'])

            values.append(datas['Take-off'])
            values.append(datas['Landing'])
            values.append(datas['Airfields']['Departure'])
            values.append(datas['Airfields']['Arrival'])
            values.append(datas['Comments'])

        self.create_flight(values)

    def calc_total_hours(self):
        t1 = timedelta(hours=self.members_hours,
                       minutes=self.members_minutes)

        t2 = timedelta(hours=self.single_engine_hours,
                       minutes=self.single_engine_minutes)

        t3 = timedelta(hours=self.multi_engines_hours,
                       minutes=self.multi_engines_minutes)

        t4 = timedelta(hours=self.ifr_hours,
                       minutes=self.ifr_minutes)

        t5 = timedelta(hours=self.simulation_hours,
                       minutes=self.simulation_minutes)

        total = t1 + t2 + t3 + t4 + t5
        return str(total)[:-3]
