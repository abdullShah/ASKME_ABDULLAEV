from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Delete all data from all tables in the database (SQLite only) except for superusers'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        user_table = User._meta.db_table

        with connection.cursor() as cursor:
            tables = connection.introspection.table_names()
            cursor.execute("PRAGMA foreign_keys = off;")

            for table in tables:
                if table == user_table:
                    self.stdout.write(f"Skipping table: {table} (preserving user data)...")
                    continue

                self.stdout.write(f"Deleting all records from table: {table}...")
                cursor.execute(f"DELETE FROM {table};")
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")

            cursor.execute("PRAGMA foreign_keys = on;")

        self.stdout.write(self.style.SUCCESS("All tables except user data have been cleared successfully!"))
