#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


from ..common import models as common_model
from ..location import models as location_model


class Holiday(common_model.TimeRecord):
    date = models.DateField()
    name = models.CharField(max_length=32)
    state = models.ForeignKey(location_model.State, null=True, blank=True)
    country = models.ForeignKey(location_model.Country, null=True, blank=True)
    description = models.TextField(default=None, null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.name