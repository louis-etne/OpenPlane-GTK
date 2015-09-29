#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from openplane import config
from datetime import timedelta
import json


class Flight:

    def __init__(self, values=None):
        if values is not None and len(values) == 19:
            self.create_flight(values)

    def create_flight(self, values):
        self.type = values[0]
        self.id = values[1]
        self.date = values[2]
        self.plane = values[3]
        self.flight_rule = values[4]

        self.departure_airfield = values[5]
        self.departure_hours = values[6]
        self.departure_minutes = values[7]

        self.arrival_airfield = values[8]
        self.arrival_hours = values[9]
        self.arrival_minutes = values[10]

        self.time_day_hours = values[11]
        self.time_day_minutes = values[12]

        self.time_night_hours = values[13]
        self.time_night_minutes = values[14]

        self.takeoffs = values[15]
        self.landings = values[16]

        self.crew = values[17]
        self.briefing = values[18]

        self.time_total_hours, self.time_total_minutes = self.total_hours()

    def save_flight(self):
        flight_name = '{}{}{}'.format(config.logbook_folder, self.date,
                                      config.flights_ext)

        flight_values = {
            'Type': self.type,
            'Id': self.id,
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
            values.append(datas['Id'])
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

            values.append(datas['Crew'])

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

    def return_total_time(self):
        if self.time_total_hours < 10:
            hours = '0{}'.format(self.time_total_hours)
        else:
            hours = str(self.time_total_hours)

        if self.time_total_minutes < 10:
            minutes = '0{}'.format(self.time_total_minutes)
        else:
            minutes = str(self.time_total_minutes)

        return ':'.join((hours, minutes))

    def return_day_time(self):
        if self.time_day_hours < 10:
            hours = '0{}'.format(self.time_day_hours)
        else:
            hours = str(self.time_day_hours)

        if self.time_day_minutes < 10:
            minutes = '0{}'.format(self.time_day_minutes)
        else:
            minutes = str(self.time_day_minutes)

        return ':'.join((hours, minutes))

    def return_night_time(self):
        if self.time_night_hours < 10:
            hours = '0{}'.format(self.time_night_hours)
        else:
            hours = str(self.time_night_hours)

        if self.time_night_minutes < 10:
            minutes = '0{}'.format(self.time_night_minutes)
        else:
            minutes = str(self.time_night_minutes)

        return ':'.join((hours, minutes))

    def return_date(self):
        year, month, day = self.date.split('-')
        if int(day) < 10:
            day = '0{}'.format(day)
        if int(month) < 10:
            month = '0{}'.format(month)
        return '/'.join((day, month, year))

    def return_day(self):
        return int(self.date.split('-')[2])

    def return_month(self):
        return int(self.date.split('-')[1]) - 1

    def return_year(self):
        return int(self.date.split('-')[0])
