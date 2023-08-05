"""
Audit models.
"""
from django.db import models

from ..settings import (
    DICTIONARIES_TIME_AUDIT_ENABLED
)


def get_dictionary_audit_mixin():
    """Get audit mixin for dictionary model."""
    if DICTIONARIES_TIME_AUDIT_ENABLED:
        return TimeAuditMixin
    else:
        return EmptyAuditMixin


def get_general_models_audit_mixin():
    """Get audit mixin for general models."""
    if DICTIONARIES_TIME_AUDIT_ENABLED:
        return TimeAuditMixin
    else:
        return EmptyAuditMixin


class EmptyAuditMixin(object):
    """Dummy audit mixin"""

    class Meta:
        abstract = True


class TimeAuditMixin(object):
    """Time audit mixin.

    Attributes:
        created_at (datetime.datetime): Creation timestamp.
        last_modified_at (datetime.datetime): Creation timestamp.
    """
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    last_modified_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True
