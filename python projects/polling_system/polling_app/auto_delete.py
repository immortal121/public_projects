from django.core.management.base import BaseCommand, CommandError
from .models import  Questions
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Delete objects older than 1 days'

    def handle(self, *args, **options):
        Questions.objects.filter(date_created__lte=datetime.now()-timedelta(days=1)).delete()
        self.stdout.write('Deleted objects older than 1 days')