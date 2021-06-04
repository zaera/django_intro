from django.core.management.base import BaseCommand
from currency_app.models import Rate
from currency_app.models import ContactUs
from faker import Faker
import random
from random import randrange


class Command(BaseCommand):
    help = 'My awesome generating data tool'    # noqa

    def handle(self, *args, **options):
        fake = Faker()
        source_list = [
            'monobank',
            'privatbank',
            'vkurse',
        ]
        for i in range(100):
            Rate.objects.create(
                moneytype='USD',
                sale=round(random.uniform(20.00, 29.99), 2),
                buy=round(random.uniform(20.00, 29.99), 2),
                source=source_list[randrange(3)],
            )
        for i in range(100):
            ContactUs.objects.create(
                 email_from=fake.free_email(),
                 subject=fake.text(max_nb_chars=50),
                 message=fake.text(max_nb_chars=200),
             )
