from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


def add_rate(source, buy, sale, moneytype):
    from currency_app.models import Rate
    from decimal import Decimal
    prev_rate = Rate.objects.filter(
        source=source,
        moneytype=moneytype
    ).order_by('created').last()
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


@shared_task
def get_currency():
    import requests
    # PRIVATBANK
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
            add_rate(source, buy, sale, moneytype)
    # MONOBANK
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
                add_rate(source, buy, sale, moneytype)
    # VKURSE
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    response.raise_for_status()
    currencies = response.json()
    needed = {'Dollar', 'Euro'}
    source = 'vkurse'
    for i in currencies:
        if i in needed:
            buy = currencies.get(i, {})['buy']
            sale = currencies.get(i, {})['sale']
            if i == 'Dollar':
                moneytype = 'USD'
            elif i == 'Euro':
                moneytype = 'EUR'
            add_rate(source, buy, sale, moneytype)
    # ABANK
    url = 'https://a-bank.com.ua/backend/api/v1/rates'
    response = requests.get(url)
    response.raise_for_status()
    currencies = response.json()
    needed = {'USD', 'EUR', 'UAH'}
    source = 'abank'
    tmp = currencies['data']
    for i in tmp:
        if i['ccyA'] in needed and i['ccyB'] in needed:
            if i['ccyB'] == 'UAH':
                buy = i['rateB']
            else:
                sale = i['rateA']
                moneytype = i['ccyB']
                add_rate(source, buy, sale, moneytype)
    # KREDOBANK
    url_usd_buy = 'https://kredobank.com.ua/api/currencies/commercial/86/buy'
    url_usd_sale = 'https://kredobank.com.ua/api/currencies/commercial/86/sale'
    url_eur_buy = 'https://kredobank.com.ua/api/currencies/commercial/87/buy'
    url_eur_sale = 'https://kredobank.com.ua/api/currencies/commercial/87/sale'
    source = 'kredobank'

    response = requests.get(url_usd_buy)
    response.raise_for_status()
    usd_buy = response.json()
    buy = float(usd_buy[-1][1]/100)

    response = requests.get(url_usd_sale)
    response.raise_for_status()
    usd_sale = response.json()
    sale = float(usd_sale[-1][1]/100)

    moneytype = 'USD'

    add_rate(source, buy, sale, moneytype)

    response = requests.get(url_eur_buy)
    response.raise_for_status()
    eur_buy = response.json()
    buy = float(eur_buy[-1][1]/100)

    response = requests.get(url_eur_sale)
    response.raise_for_status()
    eur_sale = response.json()
    sale = float(eur_sale[-1][1]/100)

    moneytype = 'EUR'

    add_rate(source, buy, sale, moneytype)
    # PIVDENNIY
    url = 'https://bank.com.ua/api/uk/v1/rest-ui/find-branch-course?date=1626210000'
    response = requests.get(url)
    response.raise_for_status()
    currencies = response.json()
    source = 'pivd'
    needed = {'USD', 'EUR'}
    for i in currencies:
        if i[1] in needed:
            buy = i[2]
            sale = i[3]
            moneytype = i[1]
            add_rate(source, buy, sale, moneytype)


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
