#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _


from ..common import models as common_model
from . import model_choices


class PhysicalBody(common_model.TimeRecord):
    height = models.DecimalField(decimal_places=3, max_digits=16, null=True, blank=True)
    height_unit = models.CharField(max_length=5, null=True, blank=True, choices=model_choices.CHOICES_HEIGHT_UNIT, default='m')
    weight = models.DecimalField(decimal_places=3, max_digits=16, null=True, blank=True)
    weight_unit = models.CharField(max_length=5, null=True, blank=True, choices=model_choices.CHOICES_WEIGHT_UNIT, default='kg')
    BMI = models.DecimalField(decimal_places=3, max_digits=16, null=True, blank=True)

    def __unicode__(self):
        return self.height


class BloodGroup(common_model.TimeRecord):
    name = models.CharField(max_length=4, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('BloodGroup')


class Gender(common_model.TimeRecord):
    name = models.CharField(max_length=2, null=True, blank=True, choices=model_choices.CHOICES_GENDER)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Gender')


class Birthday(common_model.TimeRecord):
    date = models.DateField(null=True, blank=True)
    horoscope = models.CharField(max_length=5, null=True, blank=True, choices=model_choices.CHOICES_HOROSCOPE)

    def __unicode__(self):
        return str(self.date)

    class Meta:
        verbose_name = _('Birthday')