#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _


from ..common import models as common_model


class Sqlcode(common_model.TimeRecord):
    name = models.CharField(max_length=100)
    code = models.TextField(blank=True, null=True, default='')

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = _("SQL code")
        verbose_name_plural = _("SQL codes")