import datetime

from django.utils import timezone


def json_date_to_python(json_date):
    """Convert the given `json_date` to a date object."""
    return datetime.datetime.strptime(json_date, '%Y-%m-%d').date()


def json_datetime_to_python(json_datetime):
    """Convert the given `json_datetime` to a datetime object."""
    dt = datetime.datetime.strptime(json_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")
    return timezone.make_aware(dt, timezone.utc)


def obfuscate(string):
    """Obfuscate a string by replacing all its characters except the second one."""
    obfuscation_char = '*'
    chars_to_ignore = [' ']
    return ''.join(
        char
        if i == 2 or char in chars_to_ignore else obfuscation_char
        for i, char in enumerate(string.strip(), start=1)
    )
