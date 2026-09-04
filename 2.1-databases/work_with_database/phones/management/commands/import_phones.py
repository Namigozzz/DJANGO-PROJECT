import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            # TODO: Добавьте сохранение модели
            new_phone = Phone(
                name=phone['name'],
                image=phone['image'],
                price=float(phone['price']),
                release_date=datetime.strptime(phone['release_date'], '%Y-%m-%d').date(),
                lte_exists=phone['lte_exists'].lower() == 'true',
                slug=slugify(phone['name']),
            )
            new_phone.save()
