# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models



class AutoArchiveModel(models.Model):
    """
    A model that knows how to archive itself.

    With each save where the publication status returns True,
    the full URL is submitted to an online archive.

    A reference to the archived memento is stored in a local
    database table.
    """
    # The name of the field that this model will inspect to determine
    # the object's publication status by default.
    publication_status_field = 'is_published'

    def get_publication_status(self):
        """
        Returns a boolean (True or False) indicating whether the object
        is "live" and ought to be published or not.
        Used to determine whether the save method should seek to publish,
        republish or unpublish the object when it is saved.
        By default, it looks for a BooleanField with the name defined in
        the model's 'publication_status_field'.
        If your model uses a CHOICES list of strings or other more complex
        means to indicate publication status you need to override this method
        and have it negotiate your object to return either True or False.
        """
        return getattr(self, self.publication_status_field)

    class Meta:
        abstract = True
