# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import ApiDomain


# Register your models here.

# Admin model managers for collaborate applications
@admin.register(ApiDomain)
class ApiDomainModelAdmin(admin.ModelAdmin):
    list_display = ["name", "domain", "status"]
    list_display_links = ["name"]
    search_fields = ["domain"]

    class Meta:
        model = ApiDomain
