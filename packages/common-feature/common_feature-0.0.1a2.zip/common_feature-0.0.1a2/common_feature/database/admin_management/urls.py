#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin

from ... import settings
from . import admin_views

urlpatterns = []

urlpatterns += [
    url(r'^'+settings.ADMIN_URL+'/', admin.site.urls),
    url(r'^'+settings.ADMIN_URL+'/admin-sql$', admin_views.AdminSQL.as_view()),
]