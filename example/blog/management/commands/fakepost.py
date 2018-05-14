import random
from blog.models import Post
from datetime import datetime
from django.template.defaultfilters import slugify
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        hed = "This is a random post"
        slug = slugify(hed) + "-{}".format(random.choice(range(0, 1000*1000)))
        obj = Post.objects.create(
            headline=hed,
            slug=slug,
            publication_date=datetime.now(),
            is_published=True
        )
        print("Created {}".format(obj))
