from random import randint, shuffle
from django.contrib.contenttypes.models import ContentType
from django.db import models


def get_children_of_type(parent, *types):
    if len(types) == 1:
        t = types[0]
        return t.objects.live().child_of(parent)

    content_types = tuple(ContentType.objects.get_for_model(t) for t in types)
    return parent.get_children().filter(content_type__in=content_types)
