from django.core.management.base import BaseCommand

from recipe.models import Tag

TAGS = {
    'Завтрак': ['breakfast', 'orange'],
    'Обед': ['lunch', 'green'],
    'Ужин': ['dinner', 'purple']
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for key, value in TAGS.items():
            Tag.objects.get_or_create(name=key, slug=value[0], color=value[1])
