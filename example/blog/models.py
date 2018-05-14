# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from autoarchive.models import AutoArchiveModel


class Post(AutoArchiveModel):
    """
    A blog post.
    """
    headline = models.CharField(max_length=500)
    slug = models.SlugField(unique=True)
    publication_date = models.DateField()
    is_published = models.BooleanField(default=False)
    body = models.TextField(blank=True)

    class Meta:
        ordering = ("-publication_date",)
        get_latest_by = "publication_date"

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return '/post/{}/'.format(self.slug)
