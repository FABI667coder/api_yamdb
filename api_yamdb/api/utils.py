import random
import string

from django.conf import settings


def create_conf_code():
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits,
                       k=settings.LENGTH_CONF_CODE)
    )
