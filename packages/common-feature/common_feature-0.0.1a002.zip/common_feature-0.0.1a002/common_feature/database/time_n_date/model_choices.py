#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _


# 0 - monday, 7 - sunday ... follow by datetime.date.today().weekdays()
CHOICES_DAYS = (
    ('0', _('Monday')),
    ('1', _('Tuesday')),
    ('2', _('Wednesday')),
    ('3', _('Thursday')),
    ('4', _('Friday')),
    ('5', _('Saturday')),
    ('6', _('Sunday')),
)
