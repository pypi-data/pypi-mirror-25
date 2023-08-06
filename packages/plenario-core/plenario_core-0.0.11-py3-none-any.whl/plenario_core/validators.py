import logging
import re

from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)

_starts_with_letter_regex = re.compile('^[^\d\s\-+._].*', re.UNICODE)


def starts_with_letter(value: str) -> None:
    """Validates a given value starts with any Unicode compliant letter.

    :param value: the value to validate
    :raise ValidationError: when the value doesn't start with a letter
    """
    if not _starts_with_letter_regex.match(value):
        logger.info(f'Invalid value "{value}" - does not start with letter.')
        raise ValidationError('Value must start with a letter.')
