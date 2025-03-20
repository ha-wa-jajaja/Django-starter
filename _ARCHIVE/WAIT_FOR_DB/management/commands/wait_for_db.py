"""
NOTE: Automatically to be recognized by Django as a command.
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

# NOTE: BaseCommand provides stdout and check
# NOTE: In Python, when you define a class with the syntax class a(b):, 
# it means class a inherits from class b.
class Command(BaseCommand):
    """Django command to wait for database."""

    # NOTE: handle is a requirement for Django custom management commands
    # similar to a "main" function in other programming contexts.
    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')

        db_up = False

        while db_up is False:
            try:
                # NOTE: Points to app\app\settings.py -> DATABASES.default
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))