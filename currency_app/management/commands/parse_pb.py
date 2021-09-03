from distlib.compat import raw_input
from django.core.management.base import BaseCommand
from currency_app.models import Rate
import requests
import time
from datetime import datetime
from datetime import date, timedelta
from django.utils.timezone import make_aware


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class Command(BaseCommand):
    def handle(self, *args, **options):
        day = raw_input('Enter day to start from (blank for today): ')
        month = raw_input('Enter month to start from (blank for today): ')
        year = raw_input('Enter year to start from (blank for today): ')
        if not day:
            day = date.today().day
        if not month:
            month = date.today().month
        if not year:
            year = date.today().year
        start_date = date(int(year), int(month), int(day))

        url_base = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
        end_date = date.today()
        queryset = Rate.objects.all()
        success_list = []
        unsuccess_list = []
        sleep_period = 20

        for single_date in daterange(start_date, end_date):
            url = url_base + single_date.strftime("%d.%m.%Y")
            created = datetime(single_date.year, single_date.month, single_date.day)
            print(f'Checking if {created} is already in base...') # noqa
            if not queryset.filter(created=make_aware(created)).exists():
                print(f'No record for date {created}, lets grab it!') # noqa
                print(f'Waiting for {sleep_period} seconds...') # noqa
                time.sleep(sleep_period)
                try:
                    r = requests.get(url)
                    json_ = r.json()
                    for rate in json_['exchangeRate']:
                        if 'currency' in rate:
                            if 'USD' in rate['currency']:
                                instance = Rate.objects.create(
                                    moneytype=0,
                                    sale=float(rate['saleRate']),
                                    buy=float(rate['purchaseRate']),
                                    bank_id=1,
                                    created=make_aware(created),
                                )
                                instance.created = make_aware(created)
                                instance.save(update_fields=['created'])
                                print('USD is saved') # noqa
                            elif 'EUR' in rate['currency']:
                                instance = Rate.objects.create(
                                    moneytype=1,
                                    sale=float(rate['saleRate']),
                                    buy=float(rate['purchaseRate']),
                                    bank_id=1,
                                    created=make_aware(created),
                                )
                                instance.created = make_aware(created)
                                instance.save(update_fields=['created'])
                                print('EUR is saved') # noqa
                    print('##################################################') # noqa
                    success_list.append(created)
                except Exception as e:
                    print(f'Something went wrong! {e}') # noqa
                    unsuccess_list.append(created)
            else:
                print(f'{created} record is already exists...skipping') # noqa
                print('##################################################') # noqa
        print(f'We got {len(success_list)} dates:') # noqa
        for i in range(len(success_list)):
            print(success_list[i]) # noqa
        print(f'{len(unsuccess_list)} errors in:') # noqa
        for i in range(len(unsuccess_list)):
            print(unsuccess_list[i]) # noqa
