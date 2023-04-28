import random
import string

from django.conf import settings
from django.shortcuts import get_object_or_404
from reviews.models import Title, User

def create_conf_code():
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits,
                       k=settings.LENGTH_CONF_CODE)
    )


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def __repr__(self):
        return '%s()' % self.__class__.__name__
