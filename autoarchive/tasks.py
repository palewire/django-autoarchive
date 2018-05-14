# -*- coding: utf-8 -*-
import logging
import savepagenow
from django.contrib.contenttypes.models import ContentType
logger = logging.getLogger(__name__)


def archive_object(content_type_pk, object_pk):
    """
    Archive the provided object.
    """
    from .models import Memento

    # Get the object
    ct = ContentType.objects.get_for_id(content_type_pk)
    obj = ct.get_object_for_this_type(pk=object_pk)
    logger.debug("Archiving {}".format(obj))

    # Get the URL we're going to save
    archive_url = obj.get_archive_url()

    # Archive it
    ia_url, ia_captured = savepagenow.capture_or_cache(archive_url)

    # Save the archived URL
    logger.debug("Saving memento URL {}".format(ia_url))
    ia_memento = Memento.objects.create(
        content_type=ct,
        object_pk=obj.pk,
        url=ia_url
    )
    logger.debug("Created {}".format(ia_memento))
