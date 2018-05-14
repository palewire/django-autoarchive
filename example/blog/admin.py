# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from blog import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("headline", "publication_date", "is_published")
    date_hierarchy = "publication_date"
    search = ("headline", "slug")
