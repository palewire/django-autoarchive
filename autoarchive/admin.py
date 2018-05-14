# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Memento


@admin.register(Memento)
class MementoAdmin(admin.ModelAdmin):
    list_display = ("content_object", "content_type", "timestamp", "archive")
    list_filter = ("archive",)
    date_hierarchy = "timestamp"
    readonly_fields = (
        "content_type",
        "content_object",
        "object_pk",
        "archive",
        "url"
    )
