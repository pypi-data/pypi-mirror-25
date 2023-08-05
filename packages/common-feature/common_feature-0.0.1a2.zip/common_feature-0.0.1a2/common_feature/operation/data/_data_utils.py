# -*- coding: utf-8 -*-

import datetime

from ...operation.data import _data
from ...database.physical import models as physical_model
from ...database.location import models as location_model


def create_countries():
    for country in _data._COUNTRY_LIST:
        if not location_model.Country.objects.filter(name=country).exists():
            obj = location_model.Country(name=country, status='A')
            obj.save()


def create_bloodgroup():
    for bloodgroup in _data._BLOOD_GROUP:
        if not physical_model.BloodGroup.objects.filter(name=bloodgroup['name']).exists():
            obj = physical_model.BloodGroup(name=bloodgroup['name'])
            obj.save()


def check_ZODIAC_WEST(_date=datetime.date.today()):
    _year = _date.year
    for data in _data._ZODIAC_WEST_LIST:
        start_date = datetime.date(year=_year, month=data['start_date']['month'], day=data['start_date']['day'])
        end_date = datetime.date(year=_year, month=data['end_date']['month'], day=data['end_date']['day'])
        if start_date <= _date and end_date >= _date:
            return data['name']
    return None


def check_BMI(_BMI_value):
    for data in _data._BMI_LIST:
        if data['start_value'] <= _BMI_value and data['end_value'] >= _BMI_value:
            return data['description']
    return None


def check_bloodgroup(action, bloodgroup_name):
    if action not in ('d', 'a'):
        raise Exception('action must be a-accept or d-donate')
    else:
        if action == 'a':
            value_action = 'accept'
        else:
            value_action = 'donate'
        for bloodgroup in _data._BLOOD_GROUP:
            if bloodgroup['name'] == bloodgroup_name:
                return bloodgroup[value_action]