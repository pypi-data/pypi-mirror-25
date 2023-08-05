from django.core.management.base import BaseCommand

from ...utils import seed_database


class Command(BaseCommand):
    help = 'Loads country, language, timezone data to database.'

    def handle(self, *args, **options):
        seed_database()
