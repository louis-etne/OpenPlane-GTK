#!/usr/bin/env python3
# coding: utf-8

# Made by Nodraak & Louis Etienne

import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from openplane import config

labels_airfield = (
    'Code',
    'Name',
    'MAG',
    'GEO_ARP',
    'ALT',
    'Traffic',
    'GUND',
    'Status',
)

labels_runway = (
    'Runway',
    'Surface',
    'Orientation',
    'THR_position',
    'THR_alt',
    'DTHR_position',
    'DTHR_alt',
    'Status',
)


def get_airfields():
    html = urlopen('https://www.sia.aviation-civile.gouv.fr/aip/enligne/'
                   'FRANCE/AIRAC-2015-09-17/html/eAIP/FR-AD-1.3-fr-FR.html')
    soup = BeautifulSoup(html, 'lxml')

    # Supprime toutes les balises <del></del> et leur contenu
    for d in soup.find_all('del'):
        d.decompose()

    airfields = []
    current_airfield = None

    for tr in soup.find('tbody').find_all('tr'):
        if tr.td.span.text.isalpha() or tr.td.span.text == '':
            if current_airfield is not None:
                airfields.append(current_airfield)

            # parse new airfield
            data = [':'.join(td.stripped_strings) for td in tr.find_all('td')]
            current_airfield = dict(zip(labels_airfield, data))
            current_airfield['Runways'] = []
        else:  # runway
            data = [':'.join(td.stripped_strings) for td in tr.find_all('td')]
            current_runway = dict(zip(labels_runway, data))

            current_airfield['Runways'].append(current_runway)

    # append last airfield
    airfields.append(current_airfield)
    return airfields


def parse_airfields(airfields):
    for airfield in airfields:
        if airfield['Name'] != '':
            airfield['Name'] = airfield['Name'].title()
        else:
            airfield['Name'] = None

        if airfield['Status'] != '':
            airfield['Status'] = airfield['Status'].capitalize()
        else:
            airfield['Status'] = None

        if airfield['Code'] == '':
            airfield['Code'] = None

        if airfield['Traffic'] == '':
            airfield['Traffic'] = None

        if airfield['ALT'] != '':
            airfield['ALT'] = int(airfield['ALT'])
        else:
            airfield['ALT'] = None

        if '°' in airfield['MAG']:
            airfield['MAG'] = float(airfield['MAG'].replace(':°', ''))
        else:
            airfield['MAG'] = None

        if airfield['GUND'] != 'NIL' and airfield['GUND'] != '':
            airfield['GUND'] = int(airfield['GUND'])
        else:
            airfield['GUND'] = None

        if airfield['GEO_ARP'] != '':
            airfield['GEO_ARP'] = ' '.join(airfield['GEO_ARP'].split(':'))
        else:
            airfield['GEO_ARP'] = None

        for runway in airfield['Runways']:
            # On sépare le rêvetement, la longueur et la largeur de la piste
            if runway['Surface'] != '':
                    surface_datas = runway['Surface'].split(':')

                    if 'x' in surface_datas:
                        surface_datas.remove('x')

                    runway['Length'] = int(surface_datas[0])

                    if len(surface_datas) == 3:
                        runway['Width'] = int(surface_datas[1])
                        runway['Surface'] = str(surface_datas[2]).capitalize()
                    else:
                        runway['Width'] = None
                        runway['Surface'] = str(surface_datas[1]).capitalize()
            else:
                runway['Length'] = None
                runway['Width'] = None
                runway['Surface'] = None

            if runway['Orientation'] != '':
                datas = runway['Orientation'].split(':')
                datas.remove('°')
                runway['Orientation_1'] = int(datas[0])
                runway['Orientation_2'] = int(datas[1])
                del(runway['Orientation'])
            else:
                runway['Orientation_1'] = None
                runway['Orientation_2'] = None

            if runway['Runway'] != '':
                runway['Runway_1'] = runway['Runway'].split(':')[0]
                runway['Runway_2'] = runway['Runway'].split(':')[1]
                del(runway['Runway'])
            else:
                runway['Runway_1'] = None
                runway['Runway_2'] = None
                del(runway['Runway'])

            if runway['THR_alt'] != '':
                datas = runway['THR_alt'].split(':')
                if len(datas) == 2:
                    runway['THR_alt_1'] = int(datas[0])
                    runway['THR_alt_2'] = int(datas[1])
                else:
                    runway['THR_alt_1'] = int(datas[0])
                    runway['THR_alt_2'] = int(datas[0])
                del(runway['THR_alt'])
            else:
                runway['THR_alt_1'] = None
                runway['THR_alt_2'] = None
                del(runway['THR_alt'])

            if runway['DTHR_alt'] != '':
                datas = runway['DTHR_alt'].split(':')
                if len(datas) == 2:
                    runway['DTHR_alt_1'] = int(datas[0])
                    runway['DTHR_alt_2'] = int(datas[1])
                else:
                    runway['DTHR_alt_1'] = int(datas[0])
                    runway['DTHR_alt_2'] = int(datas[0])
                del(runway['DTHR_alt'])
            else:
                runway['DTHR_alt_1'] = None
                runway['DTHR_alt_2'] = None
                del(runway['DTHR_alt'])

            if runway['THR_position'] != '':
                datas = runway['THR_position'].split(':')
                if len(datas) == 4:
                    runway['THR_position_1'] = ' '.join(datas[0:2])
                    runway['THR_position_2'] = ' '.join(datas[2:4])
                else:
                    runway['THR_position_1'] = ' '.join(datas[0:2])
                    runway['THR_position_2'] = ' '.join(datas[0:2])
                del(runway['THR_position'])
            else:
                runway['THR_position_1'] = None
                runway['THR_position_2'] = None
                del(runway['THR_position'])

            if runway['DTHR_position'] != '':
                datas = runway['DTHR_position'].split(':')
                if len(datas) == 4:
                    runway['DTHR_position_1'] = ' '.join(datas[0:2])
                    runway['DTHR_position_2'] = ' '.join(datas[2:4])
                else:
                    runway['DTHR_position_1'] = ' '.join(datas[0:2])
                    runway['DTHR_position_2'] = ' '.join(datas[0:2])
                del(runway['DTHR_position'])
            else:
                runway['DTHR_position_1'] = None
                runway['DTHR_position_2'] = None
                del(runway['DTHR_position'])

            if runway['Status'] != '':
                runway['Status'] = runway['Status'].capitalize()
            else:
                runway['Status'] = None

    return airfields


def main():
    airfields = get_airfields()
    airfields = parse_airfields(airfields)
    with open(config.airfields, 'w') as outfile:
        json.dump(airfields, outfile, ensure_ascii=True)
