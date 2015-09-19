#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from openplane import config
from datetime import timedelta
import json


class Flight:

    def __init__(self, values=None):
        if values is not None and len(values) == 21:
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

        self.comments = values[20]

    def save_flight(self):
        flight_name = '{}{}{}'.format(config.flightslog_folder, self.date,
                                      config.flights_ext)

        flight_values = {
            'Date': self.date,
            'Plane': self.plane,
            'Role': self.role,
            'Type': self.type,
            'Members': {
                'Day': self.save_time(self.members_day),
                'Night': self.save_time(self.members_night)
            },
            'Single_engine': {
                'Day': {
                    'Double': self.save_time(self.single_engine_day_double),
                    'Captain': self.save_time(self.single_engine_day_captain)
                },
                'Night': {
                    'Double': self.save_time(self.single_engine_night_double),
                    'Captain': self.save_time(self.single_engine_night_captain)
                }
            },
            'Multi_engines': {
                'Day': {
                    'Double': self.save_time(self.multi_engines_day_double),
                    'Captain': self.save_time(self.multi_engines_day_captain),
                    'Co-Pilot': self.save_time(self.multi_engines_day_copilot)
                },
                'Night': {
                    'Double': self.save_time(self.multi_engines_night_double),
                    'Captain': self.save_time(self.multi_engines_night_captain),
                    'Co-Pilot': self.save_time(self.multi_engines_night_copilot)
                }
            },
            'IFR': {
                'Double': self.save_time(self.ifr_double),
                'Captain': self.save_time(self.ifr_captain)
            },
            'Simulation': self.save_time(self.simulation),
            'IFR_arrivals': self.ifr_arrivals,
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

            values.append(datas['Comments'])

        self.create_flight(values)

    def calc_total_hours(self):
        t1_hours, t1_minutes = self.divide_time(self.members_day)
        t2_hours, t2_minutes = self.divide_time(self.members_night)
        t3_hours, t3_minutes = self.divide_time(self.single_engine_day_double)
        t4_hours, t4_minutes = self.divide_time(self.single_engine_day_captain)
        t5_hours, t5_minutes = self.divide_time(self.single_engine_night_double)
        t6_hours, t6_minutes = self.divide_time(self.single_engine_night_captain)
        t7_hours, t7_minutes = self.divide_time(self.multi_engines_day_double)
        t8_hours, t8_minutes = self.divide_time(self.multi_engines_day_captain)
        t9_hours, t9_minutes = self.divide_time(self.multi_engines_day_copilot)
        t10_hours, t10_minutes = self.divide_time(self.multi_engines_night_double)
        t11_hours, t11_minutes = self.divide_time(self.multi_engines_night_captain)
        t12_hours, t12_minutes = self.divide_time(self.multi_engines_night_copilot)
        t13_hours, t13_minutes = self.divide_time(self.ifr_double)
        t14_hours, t14_minutes = self.divide_time(self.ifr_captain)
        t15_hours, t15_minutes = self.divide_time(self.simulation)

        t1 = timedelta(hours=t1_hours , minutes=t1_minutes)
        t2 = timedelta(hours=t2_hours , minutes=t2_minutes)
        t3 = timedelta(hours=t3_hours , minutes=t3_minutes)
        t4 = timedelta(hours=t4_hours , minutes=t4_minutes)
        t5 = timedelta(hours=t5_hours , minutes=t5_minutes)
        t6 = timedelta(hours=t6_hours , minutes=t6_minutes)
        t7 = timedelta(hours=t7_hours , minutes=t7_minutes)
        t8 = timedelta(hours=t8_hours , minutes=t8_minutes)
        t9 = timedelta(hours=t9_hours , minutes=t9_minutes)
        t10 = timedelta(hours=t10_hours , minutes=t10_minutes)
        t11 = timedelta(hours=t11_hours , minutes=t11_minutes)
        t12 = timedelta(hours=t12_hours , minutes=t12_minutes)
        t13 = timedelta(hours=t13_hours , minutes=t13_minutes)
        t14 = timedelta(hours=t14_hours , minutes=t14_minutes)
        t15 = timedelta(hours=t15_hours , minutes=t15_minutes)

        total = t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9 + t10 + t11 + \
            t12 + t13 + t14 + t15

        return str(total)[:-3]

    def divide_time(self, strtime):
        '''
            Divise le temps, prend en entrée un temps de la forme hh:mm
            et sépare les heures des minutes
        '''
        hours, minutes = strtime.split(':', 1)
        return int(hours), int(minutes)

    def save_time(self, strtime):
        hours, minutes = self.divide_time(strtime)
        if hours < 10:
            hours = '0' + str(hours)  # si h = 6, retourne 06
        if minutes < 10:
            minutes = '0' + str(minutes)

        return ':'.join([str(hours), str(minutes)])
