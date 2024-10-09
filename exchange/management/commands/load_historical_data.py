import asyncio
from django.core.management.base import BaseCommand
from exchange.tasks import load_historical_data
from datetime import datetime

class Command(BaseCommand):
    help = 'Load historical exchange rates asynchronously'

    def add_arguments(self, parser):
        parser.add_argument('start_date', type=str, help='Start date in YYYY-MM-DD format')
        parser.add_argument('end_date', type=str, help='End date in YYYY-MM-DD format')

    def handle(self, *args, **kwargs):
        start_date = (datetime.strptime(kwargs['start_date'], '%Y-%m-%d')).strftime('%Y-%m-%d')
        end_date = (datetime.strptime(kwargs['end_date'], '%Y-%m-%d')).strftime('%Y-%m-%d')

        self.stdout.write(self.style.SUCCESS(f'Fetching historical rates from {start_date} to {end_date}'))

        asyncio.run(load_historical_data(start_date, end_date))

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded historical data'))