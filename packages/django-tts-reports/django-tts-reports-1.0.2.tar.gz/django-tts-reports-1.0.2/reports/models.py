# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class ApiDomain(models.Model):
    name = models.CharField(max_length=80, unique=True)
    domain = models.URLField(unique=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.domain
