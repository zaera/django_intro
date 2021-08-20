import pytest
from django.core.management import call_command


@pytest.fixture(autouse=True, scope="function")
def enable_db_access_for_all_tests(db):
    """
    give access to database for all tests
    """


@pytest.fixture(autouse=True, scope="session")
def load_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'tests/fixtures/banks.json')
        call_command('loaddata', 'tests/fixtures/rate.json')


@pytest.fixture(scope='function', autouse=True)
def fake():
    from faker import Faker
    faker = Faker()
    yield faker


@pytest.fixture(scope='function')
def client_api_auth(django_user_model):
    from rest_framework.test import APIClient
    client = APIClient()
    name = "user"
    email = "user@example.com"
    password = "password"
    user = django_user_model(email=email, password=password, username=name)
    user.set_password(password)
    user.save()
    response = client.post('/api/v1/token/', data={'username': name, 'password': password})
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer  ' + response.json()['access'])
    yield client
    user.delete()


@pytest.fixture(scope='function')
def bank():
    from currency_app.models import Bank
    yield Bank.objects.last()
