import pytest

from django.db import IntegrityError

from django_asservio_core.tests.models import (
    Code, Name,
    Description, Info
)

from .utils import check_audit_fields

pytestmark = pytest.mark.django_db


def test_code_dictionary():
    code = Code.objects.create(code='code')

    check_audit_fields(code)

    # unique constraint (`code` field)
    with pytest.raises(IntegrityError):
        Code.objects.create(code='code')


def test_name_dictionary():
    name = Name.objects.create(code='code', name='Name')

    check_audit_fields(name)

    with pytest.raises(IntegrityError):
        Name.objects.create(code='code', name='Name')


def test_description_dictionary():
    description = Description.objects.create(code='code',
                                             description='Description')

    check_audit_fields(description)

    with pytest.raises(IntegrityError):
        Description.objects.create(code='code', description='Description')


def test_regular_dictionary():
    info = Info.objects.create(code='code', name='Name',
                               description='Description')

    check_audit_fields(info)

    with pytest.raises(IntegrityError):
        Info.objects.create(code='code', name='Name',
                            description='Description')
