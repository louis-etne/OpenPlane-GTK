#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne

from urllib.request import urlopen

def get_metar(oaci):
    '''
    Récupère le metar du code oaci correspondant
    '''
    link = 'ftp://tgftp.nws.noaa.gov/data/observations/metar/stations/{}.TXT'.format(oaci.upper())

    try:
        downloaded = urlopen(link)
        metar = downloaded.read().decode('UTF-8')
    except BaseException as e:
        return None
    else:
        # On supprime le dernier '\n' et on retourne le résultat
        if metar.endswith('\n'):
            metar = metar[:-1]

        return metar


def get_taf(oaci):
    '''
    Récupère le taf du code oaci correspondant
    '''
    link = 'ftp://tgftp.nws.noaa.gov/data/forecasts/taf/stations/{}.TXT'.format(oaci.upper())
    try:
        downloaded = urlopen(link)
        taf = downloaded.read().decode('UTF-8')
    except BaseException as e:
        return None
    else:
        # On supprime le dernier '\n' et on retourne le résultat
        if taf.endswith('\n'):
            taf = taf[:-1]

        return taf