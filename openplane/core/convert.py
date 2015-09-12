#!/usr/bin/env python3
# coding: utf-8

# Made by Louis Etienne


##
# Unitées supportées : m, km, ft, mn, F°, C°, K°
##


#########
# GÉNÉRAL
##


def kilometers2meters(kilometers):
    return round(kilometers * 1000, 2)


def meters2kilometers(meters):
    return round(meters / 1000, 2)


###########
# DISTANCES
##


def kilometers2miles(kilometers):
    return round(kilometers / 1.852, 2)


def meters2miles(meters):
    return round(meters * 0.00062137, 2)


def miles2kilometers(miles):
    return round(miles * 1.852, 2)


def miles2meters(miles):
    return round(miles / 0.00062137, 2)


###########
# ALTITUDES
##


def meters2feet(meters):
    return round(meters * 3.2808, 2)


def kilometers2feet(kilometers):
    return round(kilometers * 3280.8, 2)


def miles2feet(miles):
    return round(miles * 0.00018939, 2)


def feet2meters(feet):
    return round(feet / 3.2808, 2)


def feet2kilometers(feet):
    return round(feet / 3280.8, 2)


def feet2miles(feet):
    return round(feet / 0.00018939, 2)


##############
# TEMPÉRATURES
##


def celsius2fahrenheit(celsius):
    return round((celsius * 1.8) + 32.0, 2)


def celsius2kelvin(celsius):
    return round(celsius + 273.15, 2)


def fahrenheit2celsius(fahrenheit):
    return round((fahrenheit - 32.0) / 1.8, 2)


def fahrenheit2kelvin(fahrenheit):
    return round((fahrenheit - 32) / 1.8 + 273.15, 2)


def kelvin2celsius(kelvin):
    return round(kelvin - 273.15, 2)


def kelvin2fahrenheit(kelvin):
    return round((kelvin - 273.15) * 1.8 + 32.0, 2)
