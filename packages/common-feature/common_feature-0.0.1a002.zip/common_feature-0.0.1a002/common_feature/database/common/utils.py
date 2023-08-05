#!/usr/bin/env python
# -*- coding: utf-8 -*-
from redis import StrictRedis
import redis_lock
from django.db.models import F


from . import models


class Lock(object):
    @staticmethod
    def obtain_lock(name):
        try:
            lock = models.Lock.objects.get(name=name)
            lock.counter = F('counter') + 1
            lock.save()
        except models.Lock.DoesNotExist:
            lock = models.Lock(name=name, counter=1)
            lock.save()

    @staticmethod
    def reset_locks():
        conn = StrictRedis()
        redis_lock.reset_all(conn)