import re
import datetime as dt

from django.core.exceptions import ValidationError


class UsernameValidator:
    regex = r'^[\w.@+-]+$'

    def __init__(self, forbidden_name='me'):
        self.forbidden_name = forbidden_name

    def __call__(self, value):
        if value == self.forbidden_name:
            raise ValidationError(
                'This username is not allowed.'
            )
        if not re.match(self.regex, value):
            raise ValidationError(
                'Letters or symbols: .@+- only.'
            )


def validate_year(year):
    now_year = dt.datetime.now().year
    if year > now_year:
        raise ValidationError(
            'The year cannot be longer than the current one'
        )
