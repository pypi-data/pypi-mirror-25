#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class TimeRecord(models.Model):  # use to record time create or modified every model save
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    active_status = models.BooleanField(default=True)  # true - allow to use
    comment = models.TextField(verbose_name="Comments", blank=True, null=True)
    user = models.ForeignKey(User, default='', null=True, blank=True, db_index=True)

    class Meta:
        abstract = True


class Lock(TimeRecord):  # use to lock transaction or multi action
    name = models.CharField(max_length=32, null=False, blank=False, unique=True, db_index=True)
    counter = models.BigIntegerField(blank=False, null=False, default=0)

    class Meta:
        verbose_name = _('Lock')