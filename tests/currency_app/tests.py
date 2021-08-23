import pytest
from django.core.mail import send_mail

from currency_app.models import Bank


@pytest.mark.skip('just an example')
def fake_test(client):
    response = client.get('/')
    assert response.status_code == 200


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.templates[0].name == 'index.html'
    assert [t.name for t in response.templates] == ['index.html', 'template.html']


def test_rate_list(client):
    response = client.get('/currency/rate/list/')
    assert response.status_code == 200


def test_create_bank_get_form(client):
    response = client.get('/currency/bank/create/')
    assert response.status_code == 200


def test_create_bank_empty_form_data(client):
    response = client.post('/currency/bank/create/')
    assert response.status_code == 200
    assert response.context['form'].errors == {
        'name': ['This field is required.'],
        'url': ['This field is required.']
    }


def test_create_bank_invalid_form_data(client):
    rates_intial_cpunt = Bank.objects.count()
    form_data = {
        'name': 0,
        'url': 0,
    }
    response = client.post('/currency/bank/create/', data=form_data)
    assert response.status_code == 200
    assert response.context['form'].errors == {'url': ['Enter a valid URL.']}
    assert Bank.objects.count() == rates_intial_cpunt


def test_create_bank_valid_form_data(client):
    rates_intial_cpunt = Bank.objects.count()
    form_data = {
        'name': 'fvsdczxsf!@!@#@%^&*()$%$^$&*^&@#!',
        'url': 'http://www.test.test/',
    }
    responce = client.post('/currency/bank/create/', data=form_data)
    assert responce.status_code == 302
    assert Bank.objects.count() == rates_intial_cpunt + 1


def test_registration(client, mailoutbox, settings):
    email = '1user123@mail.com'
    form_data = {
        'email': email,
        'username': '1user123',
        'password1': 'password1',
        'password2': 'password1',
    }
    response = client.post('/accounts/signup/', data=form_data)
    assert response.status_code == 302
    assert response.url == '/'
    if response.status_code == 302:
        title = 'Activate your account'
        send_mail(
            title,
            'body',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        assert mail.to == [email]
        assert mail.subject == title
