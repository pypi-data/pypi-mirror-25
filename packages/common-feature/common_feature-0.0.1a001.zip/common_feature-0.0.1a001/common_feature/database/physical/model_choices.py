#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _


CHOICES_GENDER = (
    ('N/A', _('None')),
    ('M', _('Male')),
    ('F', _('Female')),
)

CHOICES_BLOODGROUP = (
    ('N/A', 'None'),
    ('A', 'A'),
    ('B', 'B'),
    ('O', 'O'),
    ('AB', 'AB'),
    ('A+', 'A+'),
    ('B+', 'B+'),
    ('O+', 'O+'),
    ('AB+', 'AB+'),
    ('A-', 'A-'),
    ('B-', 'B-'),
    ('O-', 'O-'),
    ('AB-', 'AB-'),
)

CHOICES_HOROSCOPE = (
    ('AQU', 'Aquarius'),
    ('PIS', 'Pisces'),
    ('ARI', 'Aries'),
    ('TAU', 'Taurus'),
    ('GEM', 'Gemini'),
    ('CAN', 'Cancer'),
    ('LEO', 'Leo'),
    ('VIR', 'Virgo'),
    ('LIB', 'Libra'),
    ('SCO', 'Scorpio'),
    ('SAG', 'Sagittarius'),
    ('CAP', 'Capricorn'),
)


CHOICES_HEIGHT_UNIT = (
    ('cm', 'centimeter'),
    ('m', 'meter'),
)


CHOICES_WEIGHT_UNIT = (
    ('g', 'gram'),
    ('kg', 'kilogram'),
)