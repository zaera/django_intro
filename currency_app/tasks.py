from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from currency_app import consts, choices


def add_rate(source, buy, sale, moneytype):
    from currency_app.models import Rate, Bank
    from decimal import Decimal
    bank = Bank.objects.get(code_name=source)
    prev_rate = Rate.objects.filter(
        bank=bank,
        moneytype=moneytype,

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
            bank=bank,
        )


def get_pb():
    from currency_app.models import Bank
    source = consts.CODE_NAME_PRIVATBANK
    bank = Bank.objects.get(code_name=consts.CODE_NAME_PRIVATBANK)
    import requests
    response = requests.get(bank.url)
    response.raise_for_status()
    currencies = response.json()
    needed = {'USD', 'EUR'}
    for i in currencies:
        if i['ccy'] in needed:
            buy = i['buy']
            sale = i['sale']
            if i['ccy'] == 'USD':
                moneytype = choices.RATE_TYPE_USD
            elif i['ccy'] == 'EUR':
                moneytype = choices.RATE_TYPE_EUR
            add_rate(source, buy, sale, moneytype)


def get_mono():
    import requests
    from currency_app.models import Bank
    source = consts.CODE_NAME_MONOBANK
    bank = Bank.objects.get(code_name=consts.CODE_NAME_MONOBANK)
    response = requests.get(bank.url)
    response.raise_for_status()
    currencies = response.json()
    needed = {840, 978}
    source = consts.CODE_NAME_MONOBANK
    for i in currencies:
        if i['currencyCodeA'] in needed:
            if i['currencyCodeB'] == 980:
                buy = i['rateBuy']
                sale = i['rateSell']
                if i['currencyCodeA'] == 840:
                    moneytype = choices.RATE_TYPE_USD
                elif i['currencyCodeA'] == 978:
                    moneytype = choices.RATE_TYPE_EUR
                add_rate(source, buy, sale, moneytype)


def get_vkurse():
    import requests
    from currency_app.models import Bank
    source = consts.CODE_NAME_VKURSE
    bank = Bank.objects.get(code_name=consts.CODE_NAME_VKURSE)
    response = requests.get(bank.url)
    response.raise_for_status()
    currencies = response.json()
    needed = {'Dollar', 'Euro'}
    source = consts.CODE_NAME_VKURSE
    for i in currencies:
        if i in needed:
            buy = currencies.get(i, {})['buy']
            sale = currencies.get(i, {})['sale']
            if i == 'Dollar':
                moneytype = choices.RATE_TYPE_USD
            elif i == 'Euro':
                moneytype = choices.RATE_TYPE_EUR
            add_rate(source, buy, sale, moneytype)


def get_abank():
    import requests
    from currency_app.models import Bank
    source = consts.CODE_NAME_ABANK
    bank = Bank.objects.get(code_name=consts.CODE_NAME_ABANK)
    response = requests.get(bank.url)
    response.raise_for_status()
    currencies = response.json()
    needed = {'USD', 'EUR', 'UAH'}
    source = consts.CODE_NAME_ABANK
    tmp = currencies['data']
    for i in tmp:
        if i['ccyA'] in needed and i['ccyB'] in needed:
            if i['ccyB'] == 'UAH':
                buy = i['rateB']
            else:
                sale = i['rateA']
                if i['ccyB'] == 'USD':
                    moneytype = choices.RATE_TYPE_USD
                elif i['ccyB'] == 'EUR':
                    moneytype = choices.RATE_TYPE_EUR
                add_rate(source, buy, sale, moneytype)


def get_kredo():
    import requests
    from currency_app.models import Bank
    source = consts.CODE_NAME_KREDOBANK
    bank = Bank.objects.get(code_name=consts.CODE_NAME_KREDOBANK)
    url_usd_buy = bank.url + '86/buy'
    url_usd_sale = bank.url + '86/sale'
    url_eur_buy = bank.url + '87/buy'
    url_eur_sale = bank.url + '87/sale'
    source = consts.CODE_NAME_KREDOBANK

    response = requests.get(url_usd_buy)
    response.raise_for_status()
    usd_buy = response.json()
    buy = float(usd_buy[-1][1] / 100)

    response = requests.get(url_usd_sale)
    response.raise_for_status()
    usd_sale = response.json()
    sale = float(usd_sale[-1][1] / 100)

    moneytype = choices.RATE_TYPE_USD

    add_rate(source, buy, sale, moneytype)

    response = requests.get(url_eur_buy)
    response.raise_for_status()
    eur_buy = response.json()
    buy = float(eur_buy[-1][1] / 100)

    response = requests.get(url_eur_sale)
    response.raise_for_status()
    eur_sale = response.json()
    sale = float(eur_sale[-1][1] / 100)

    moneytype = choices.RATE_TYPE_EUR

    add_rate(source, buy, sale, moneytype)


def get_pivdenniy():
    import requests
    from currency_app.models import Bank
    source = consts.CODE_NAME_PIVDENNIY
    bank = Bank.objects.get(code_name=consts.CODE_NAME_PIVDENNIY)
    response = requests.get(bank.url)
    response.raise_for_status()
    currencies = response.json()
    source = consts.CODE_NAME_PIVDENNIY
    needed = {'USD', 'EUR'}
    for i in currencies:
        if i[1] in needed:
            buy = i[2]
            sale = i[3]
            if i[1] == 'USD':
                moneytype = choices.RATE_TYPE_USD
            elif i[1] == 'EUR':
                moneytype = choices.RATE_TYPE_EUR
            add_rate(source, buy, sale, moneytype)


@shared_task
def get_currency():
    get_pb()
    get_mono()
    get_vkurse()
    get_abank()
    get_kredo()
    get_pivdenniy()


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
