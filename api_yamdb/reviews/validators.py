from django.core.validators import RegexValidator


class UsernameValidator(RegexValidator):
    regex = r'^[\w.@+-]+$'
    message = 'Only digits or letters or symbols :@/./+/-/_'
