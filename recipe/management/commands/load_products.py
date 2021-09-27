import csv
import os

from django.core.management.base import BaseCommand

from foodgram.settings import BASE_DIR
from recipe.models import Product

CSV_FILE_PATH = os.path.join(BASE_DIR, 'staticfiles/ingredients.csv')


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH, encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                title, dimension = row
                Product.objects.get_or_create(
                    title=title, dimension=dimension
                    )
