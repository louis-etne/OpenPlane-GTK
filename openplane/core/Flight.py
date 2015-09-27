#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from openplane import config
from datetime import timedelta
import json


class Flight:

    def __init__(self, values=None):
        if values is not None and len(values) == 18:
            self.create_flight(values)

    def create_flight(self, values):
        self.type = values[0]
        self.date = values[1]
        self.plane = values[2]
        self.flight_rule = values[3]

        self.departure_airfield = values[4]
        self.departure_hours = values[5]
        self.departure_minutes = values[6]

        self.arrival_airfield = values[7]
        self.arrival_hours = values[8]
        self.arrival_minutes = values[9]

        self.time_day_hours = values[10]
        self.time_day_minutes = values[11]

        self.time_night_hours = values[12]
        self.time_night_minutes = values[13]

        self.takeoffs = values[14]
        self.landings = values[15]

        self.crew = values[16]
        self.briefing = values[17]

        self.time_total_hours, self.time_total_minutes = self.total_hours()

    def save_flight(self):
        flight_name = '{}{}{}'.format(config.logbook_folder, self.date,
                                      config.flights_ext)

        flight_values = {
            'Type': self.type,
            'Date': self.date,
            'Plane': self.plane,
            'Flight_rule': self.flight_rule,
            'Departure': {
                'Airfield': self.departure_airfield,
                'Hours': self.departure_hours,
                'Minutes': self.departure_minutes
            },
            'Arrival': {
                'Airfield': self.arrival_airfield,
                'Hours': self.arrival_hours,
                'Minutes': self.arrival_minutes
            },
            'Times': {
                'Day': {
                    'Hours': self.time_day_hours,
                    'Minutes': self.time_day_minutes
                },
                'Night': {
                    'Hours': self.time_night_hours,
                    'Minutes': self.time_night_minutes
                },
                'Total': {
                    'Hours': self.time_total_hours,
                    'Minutes': self.time_total_minutes
                }
            },
            'Operations': {
                'Takeoffs': self.takeoffs,
                'Landings': self.landings
            },
            'Crew': self.crew,
            'Briefing': self.briefing
        }

        with open(flight_name, 'w') as outfile:
            json.dump(flight_values, outfile, indent=4, sort_keys=True)

    def import_flight(self, filepath):
        values = []

        with open(filepath, 'r') as reader:
            datas = json.load(reader)

            values.append(datas['Type'])
            values.append(datas['Date'])
            values.append(datas['Plane'])
            values.append(datas['Flight_rule'])

            values.append(datas['Departure']['Airfield'])
            values.append(datas['Departure']['Hours'])
            values.append(datas['Departure']['Minutes'])

            values.append(datas['Arrival']['Airfield'])
            values.append(datas['Arrival']['Hours'])
            values.append(datas['Arrival']['Minutes'])

            values.append(datas['Times']['Day']['Hours'])
            values.append(datas['Times']['Day']['Minutes'])
            values.append(datas['Times']['Night']['Hours'])
            values.append(datas['Times']['Night']['Minutes'])

            values.append(datas['Operations']['Takeoffs'])
            values.append(datas['Operations']['Landings'])

            values.append['Crew']

            values.append(datas['Briefing'])

        self.create_flight(values)

    def total_hours(self):
        t_day = timedelta(hours=self.time_day_hours,
                       minutes=self.time_day_minutes)

        t_night = timedelta(hours=self.time_night_hours,
                       minutes=self.time_night_minutes)

        total = str(t_day + t_night)[:-3]
        hours, minutes = total.split(':')
        return int(hours), int(minutes)
