#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..common import models as common_model


class Country(common_model.TimeRecord):
    name = models.CharField(max_length=128, unique=True, verbose_name=_('country'), help_text=_('country_help_text'),
                            null=False, blank=False, db_index=True)
    country_code = models.CharField(max_length=12, default='', blank=True, null=True)
    flag_pic = models.ImageField(default='', upload_to='django_common_feature/location/country/', null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _('Countries')


class State(common_model.TimeRecord):
    country = models.ForeignKey("Country", null=True, blank=True)
    name = models.CharField(max_length=128, unique=True, verbose_name=_('state'), help_text=_('state_help_text'),
                            null=False, blank=False, db_index=True)

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _('States')