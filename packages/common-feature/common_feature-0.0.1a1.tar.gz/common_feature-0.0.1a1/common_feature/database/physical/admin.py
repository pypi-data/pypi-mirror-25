#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib import admin

from . import models


@admin.register(models.Birthday)
class BirthdayAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if obj.date:
            pass
        obj.save()