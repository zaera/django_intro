from django.apps import AppConfig
from django.db import connection


class CurrencyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'currency_app'

    def ready(self):
        from currency_app.models import Bank
        from currency_app import consts

        all_tables = connection.introspection.table_names()

        # check if table exists
        # table could be absent before initial migration
        # if Bank._meta.db_table in all_tables:
        if 'currency_app_bank' in all_tables:
            try:
                print('Update Banks Initial Data') # noqa
                code_name = consts.CODE_NAME_PRIVATBANK
                pb_data = {
                    'name': 'PrivatBank',
                    'url': 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5',
                    'original_url': 'https://www.privat24.ua/',
                }
                Bank.objects.update_or_create(code_name=code_name, defaults=pb_data)

                code_name = consts.CODE_NAME_MONOBANK
                mono_data = {
                    'name': 'Monobank',
                    'url': 'https://api.monobank.ua/bank/currency',
                    'original_url': 'https://www.monobank.ua/',
                }
                Bank.objects.update_or_create(code_name=code_name, defaults=mono_data)

                code_name = consts.CODE_NAME_VKURSE
                vkurse_data = {
                    'name': 'Monobank',
                    'url': 'http://vkurse.dp.ua/course.json',
                    'original_url': 'http://vkurse.dp.ua/',
                }
                Bank.objects.update_or_create(code_name=code_name, defaults=vkurse_data)

                code_name = consts.CODE_NAME_ABANK
                abank_data = {
                    'name': 'Abank',
                    'url': 'https://a-bank.com.ua/backend/api/v1/rates',
                    'original_url': 'https://a-bank.com.ua/',
                }
                Bank.objects.update_or_create(code_name=code_name, defaults=abank_data)

                code_name = consts.CODE_NAME_KREDOBANK
                kredo_data = {
                    'name': 'Kredobank',
                    'url': 'https://kredobank.com.ua/api/currencies/commercial/',
                    'original_url': 'https://kredobank.com.ua/',
                }
                Bank.objects.update_or_create(code_name=code_name, defaults=kredo_data)

                code_name = consts.CODE_NAME_PIVDENNIY
                kredo_data = {
                    'name': 'Pivdenniy',
                    'url': 'https://bank.com.ua/api/uk/v1/rest-ui/find-branch-course?date=0',
                    'original_url': 'https://bank.com.ua/',
                }
                Bank.objects.update_or_create(code_name=code_name, defaults=kredo_data)
            except:
                print('failed here after clean migration')
            
