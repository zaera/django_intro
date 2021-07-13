from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def get_currency():
    from currency_app.models import Rate
    import requests
    from decimal import Decimal

    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    response.raise_for_status()
    currencies = response.json()
    needed = {'USD', 'EUR'}
    source = 'privatbank'
    for i in currencies:
        if i['ccy'] in needed:
            buy = i['buy']
            sale = i['sale']
            moneytype = i['ccy']
            prev_rate = Rate.objects.filter(source=source, moneytype=moneytype).order_by('created').last()
            if (
                    prev_rate is None
                    or prev_rate.sale != Decimal(sale).quantize(Decimal('0.01'))
                    or prev_rate.buy != Decimal(buy).quantize(Decimal('0.01'))
            ):                Rate.objects.create(
                    buy=buy,
                    sale=sale,
                    moneytype=moneytype,
                    source=source,
                )
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    response.raise_for_status()
    currencies = response.json()
    needed = {840, 978}
    source = 'monobank'
    for i in currencies:
        if i['currencyCodeA'] in needed:
            if i['currencyCodeB'] == 980:
                buy = i['rateBuy']
                sale = i['rateSell']
                if i['currencyCodeA'] == 840:
                    moneytype = 'USD'
                elif i['currencyCodeA'] == 978:
                    moneytype = 'EUR'
                prev_rate = Rate.objects.filter(source=source, moneytype=moneytype).order_by('created').last()
                if (
                        prev_rate is None
                        or prev_rate.sale != Decimal(sale).quantize(Decimal('0.01'))
                        or prev_rate.buy != Decimal(buy).quantize(Decimal('0.01'))
                ):
                    Rate.objects.create(
                        buy=buy,
                        sale=sale,
                        moneytype=moneytype,
                        source=source,
                    )
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    response.raise_for_status()
    currencies = response.json()
    needed = {'Dollar', 'Euro'}
    source = 'vkurse'
    for i in currencies:
        if i in needed:
            type = i
            if type in needed:
                buy = currencies.get(i, {})['buy']
                sale = currencies.get(i, {})['sale']
                if i == 'Dollar':
                    moneytype = 'USD'
                elif i == 'Euro':
                    moneytype = 'EUR'
                print(buy)
                print(sale)
                print(moneytype)
                prev_rate = Rate.objects.filter(source=source, moneytype=moneytype).order_by('created').last()
                if (
                        prev_rate is None
                        or prev_rate.sale != Decimal(sale).quantize(Decimal('0.01'))
                        or prev_rate.buy != Decimal(buy).quantize(Decimal('0.01'))
                ):
                    Rate.objects.create(
                        buy=buy,
                        sale=sale,
                        moneytype=moneytype,
                        source=source,
                    )

# @shared_task
# def get_mono():
#     from currency_app.models import Rate
#     import requests
#     url = 'https://api.monobank.ua/bank/currency'
#     response = requests.get(url)
#     response.raise_for_status()
#     currencies = response.json()
#     needed = {840, 978}
#     source = 'monobank'
#     for i in currencies:
#         if i['currencyCodeA'] in needed:
#             if i['currencyCodeB'] == 980:
#                 buy = i['rateBuy']
#                 sale = i['rateSell']
#                 if i['currencyCodeA'] == 840:
#                     moneytype = 'USD'
#                 elif i['currencyCodeA'] == 978:
#                     moneytype = 'EUR'
#                 Rate.objects.create(
#                     buy=buy,
#                     sale=sale,
#                     moneytype=moneytype,
#                     source=source,
#                 )


@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={
        'max_retries': 5,
        'default_retry_delay': 60,
    },
)
def send_mail_in_bckg(data_subject, data_email_from):
    send_mail(
        data_subject,
        'Thank you for your attention!\nWe will get back shortly with the answer to you!',
        settings.DEFAULT_FROM_EMAIL,
        [data_email_from],
        fail_silently=False,
    )


#a-bank
#https://a-bank.com.ua/backend/api/v1/rates

# kredobank  https://kredobank.com.ua/info/kursy-valyut/commercial
# USD
# https://kredobank.com.ua/api/currencies/commercial/86/buy
# https://kredobank.com.ua/api/currencies/commercial/86/sale
# EUR
# https://kredobank.com.ua/api/currencies/commercial/87/buy
# https://kredobank.com.ua/api/currencies/commercial/87/sale