#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models

@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    pass