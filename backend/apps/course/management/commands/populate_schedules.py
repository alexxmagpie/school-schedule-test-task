from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from apps.course.factories import ScheduleFactory


class Command(BaseCommand):
    help = 'Populates the database with apps.course.models.Schedule test objects using Factory Boy'

    def add_arguments(self, parser):
        parser.add_argument(
            'num_records',
            type=int,
            help='The number of records to create in the database'
        )

    def handle(self, *args, **kwargs):
        num_records = kwargs.get('num_records', 10)
        self.stdout.write(self.style.SUCCESS(f'Starting to populate the database with {num_records} records...'))
        try:
            ScheduleFactory.create_batch(num_records)
        except IntegrityError:
            self.stdout.write(self.style.SUCCESS('IntegrityError occurred... Database may be populated partionally.'))
        else:
            self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
