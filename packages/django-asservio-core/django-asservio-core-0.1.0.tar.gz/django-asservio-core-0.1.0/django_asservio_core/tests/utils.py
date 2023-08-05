"""
Test utilities.
"""
from django.conf import settings

DICTIONARIES_TIME_AUDIT_ENABLED = \
    getattr(settings, 'CORE_DICTIONARIES_TIME_AUDIT_ENABLED', False)


def check_audit_fields(instance):
    """
    Args:
        instance (django.db.models.Model): Some instance. 
    """
    assert hasattr(instance, 'created_at') \
           == DICTIONARIES_TIME_AUDIT_ENABLED

    assert hasattr(instance, 'last_modified_at') \
           == DICTIONARIES_TIME_AUDIT_ENABLED
