# Generated by Django 3.2.3 on 2021-07-20 17:05

from django.db import migrations


def forwards(apps, schema_editor):
    Rate = apps.get_model('currency_app', 'Rate')
    Bank = apps.get_model('currency_app', 'Bank')
    privatbank = Bank.objects.create(
        name='Privatbank',
        url='https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5',
        origin_url='https://www.privat24.ua/',)
    for rate in Rate.objects.all():
        if 'privatbank' in rate.source.lower():
            rate.bank = privatbank

        rate.save()


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('currency_app', '0005_auto_20210720_1513'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
