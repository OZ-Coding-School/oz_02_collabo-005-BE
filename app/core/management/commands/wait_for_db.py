from django.core.management.base import BaseCommand
from django.db import connections
import time
from django.db.utils import OperationalError
from MySQLdb import OperationalError as MySQLdbOperationalError

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for DB connection ...')

        is_db_connected = None
        while not is_db_connected:
            try:
                # 'default'는 settings.py의 DATABASES 설정에 정의된 이름입니다.
                is_db_connected = connections['default']
            except (OperationalError, MySQLdbOperationalError):
                self.stdout.write("Retrying DB connection ...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Congratulations! MySQL Connection Success!!!"))
