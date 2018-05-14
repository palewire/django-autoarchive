# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from autoarchive import tasks
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.encoding import python_2_unicode_compatible


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

        Used to determine whether the save method related to a published object.

        By default, it looks for a BooleanField with the name defined in
        the model's 'publication_status_field'. The default is `is_published`.

        If the attribute doesn't exist, the object is archived on every save.

        If your model uses a CHOICES list of strings or other more complex
        means to indicate publication status you need to override this method
        and have it negotiate your object to return either True or False.
        """
        return getattr(self, self.publication_status_field, True)

    def get_archive_url(self):
        """
        Returns the URL that should be archived for each object.

        By default, it combines `get_absolute_url` with the site's domain.

        Override this function to provide your own custom URL.
        """
        if not hasattr(self, 'get_absolute_url'):
            raise NotImplementedError("Set get_absolute_url or override get_archive_url to set the URL to archive.")
        try:
            from django.contrib.sites.models import Site
            domain = Site.objects.get_current().domain
        except RuntimeError:
            raise NotImplementedError("Install Django's sites app or override get_archive_url to set domain to archive.")
        return 'http://%s%s' % (domain, self.get_absolute_url())

    def save(self, *args, **kwargs):
        """
        A custom save that archives the object where appropriate.

        Save with keyword argument obj.save(archive=False) to skip the process.
        """
        # if obj.save(archive=False) has been passed, we skip everything.
        if not kwargs.pop('archive', True):
            super(AutoArchiveModel, self).save(*args, **kwargs)
        # Otherwise, for the standard obj.save(), here we go...
        else:
            # Save the object
            super(AutoArchiveModel, self).save(*args, **kwargs)
            # If it's published, archive it
            if self.get_publication_status():
                ct = ContentType.objects.get_for_model(self.__class__)
                tasks.archive_object(ct.pk, self.pk)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Memento(models.Model):
    """
    A reference to an archived version of a model object.
    """
    timestamp = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
    )

    # Content-object field
    content_type = models.ForeignKey(
        ContentType,
        verbose_name='content type',
        related_name="content_type_set_for_%(class)s",
        on_delete=models.CASCADE
    )
    object_pk = models.TextField(verbose_name='object ID')
    content_object = GenericForeignKey(
        ct_field="content_type",
        fk_field="object_pk"
    )

    # The archived url
    ARCHIVE_CHOICES = (
        ('archive.org', 'archive.org'),
    )
    archive = models.CharField(
        max_length=1000,
        choices=ARCHIVE_CHOICES,
        db_index=True,
        default=ARCHIVE_CHOICES[0][0],
    )
    url = models.URLField(max_length=1000)

    class Meta:
        ordering = ("-timestamp",)
        get_latest_by = 'timestamp'

    def __str__(self):
        return self.url
