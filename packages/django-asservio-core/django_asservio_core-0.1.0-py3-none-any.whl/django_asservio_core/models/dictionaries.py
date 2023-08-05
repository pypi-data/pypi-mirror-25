"""
Dictionaries models.
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..settings import (
    DICTIONARIES_CODE_MAX_LENGTH,
    DICTIONARIES_NAME_MAX_LENGTH,
    DICTIONARIES_DESCRIPTION_MAX_LENGTH
)

from .audit import (
    get_dictionary_audit_mixin
)

AUDIT_MIXIN = get_dictionary_audit_mixin()


class CodeDictionary(AUDIT_MIXIN, models.Model):
    """Abstract class for code dictionaries
        (contains only field `code`).

    Attributes:
        id (int): ID.
        code (str): Code.
    """
    code = models.CharField(
        verbose_name=_('Code'),
        max_length=DICTIONARIES_CODE_MAX_LENGTH,
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.code


class NameDictionary(CodeDictionary):
    """Abstract class for description dictionaries
        (contain fields `code` and `name`).

    Attributes:
        id (int): ID.
        code (str): Code.
        name (str): Name.
    """
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=DICTIONARIES_NAME_MAX_LENGTH
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.code


class DescriptionDictionary(CodeDictionary):
    """Abstract class for description dictionaries
        (contain fields `code` and `description`).

    Attributes:
        id (int): ID.
        code (str): Code.
        description (str): Description.
    """
    description = models.CharField(
        verbose_name=_('Description'),
        max_length=DICTIONARIES_DESCRIPTION_MAX_LENGTH,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.code


class Dictionary(DescriptionDictionary):
    """Abstract class for regular dictionaries
        (contain fields `name`, `code` and `description`).

    Attributes:
        id (int): ID.
        name (str): Name.
        code (str): Code.
        description (str): Description.
    """
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=DICTIONARIES_NAME_MAX_LENGTH
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.code
