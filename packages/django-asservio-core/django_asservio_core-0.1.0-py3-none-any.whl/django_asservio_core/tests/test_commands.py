import logging

import pytest

from django_asservio_core.utils import seed_database


@pytest.mark.django_db
def test_seed_database():
    seed_database()
