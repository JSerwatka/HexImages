from django.core.validators import RegexValidator
from django.utils.regex_helper import _lazy_re_compile


def positive_int_list_validator(message=None, code='invalid'):
    regexp = _lazy_re_compile(r'^[1-9]\d*(?:,[1-9]\d*)*\Z')
    return RegexValidator(regexp, message=message, code=code)