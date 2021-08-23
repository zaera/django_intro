from currency_app import choices
from currency_app.models import Rate


def test_rates_list(client_api_auth):
    response = client_api_auth.get('/api/v1/rates/')
    assert response.status_code == 200
    assert 'results' in response.json()


def test_rates_invalid_post(client_api_auth):
    post_data = {
        "buy": "99.99",
        "bank": 1,
        "moneytype": 1
    }
    response = client_api_auth.post(
        "/api/v1/rates/",
        data=post_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400
    assert response.json()


def test_rates_empty_post(client_api_auth):
    response = client_api_auth.post(
        "/api/v1/rates/",
        data={},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400
    assert response.json() == {
        "sale": [
            "This field is required."
        ],
        "buy": [
            "This field is required."
        ],
        "bank": [
            "This field is required."
        ],
        "moneytype": [
            "This field is required."
        ]
    }


def test_rates_valid_post(client_api_auth, bank):
    initial_count = Rate.objects.count()
    post_data = {
        "sale": "99.99",
        "buy": "99.99",
        "bank": bank.id,
        "moneytype": choices.RATE_TYPE_EUR
    }
    response = client_api_auth.post(
        "/api/v1/rates/",
        data=post_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201
    assert response.json()
    assert Rate.objects.count() == initial_count + 1


def test_rates_delete(client_api_auth):
    initial_count = Rate.objects.count()
    rate = Rate.objects.last()
    response = client_api_auth.delete(f"/api/v1/rates/{rate.id}/", )
    assert response.status_code == 204
    assert Rate.objects.count() == initial_count - 1


def test_rates_update(client_api_auth):
    rate = Rate.objects.last()
    post_data = {
        "buy": "199.99"
    }
    response = client_api_auth.patch(
        f"/api/v1/rates/{rate.id}/",
        data=post_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json()['buy'] == '199.99'


def test_rates_doesnot_exist(client_api_auth):
    non_existing_id = Rate.objects.count() + 1
    response = client_api_auth.get(
        f"/api/v1/rates/{non_existing_id}/", )
    assert response.status_code == 404
    assert response.json()['detail'] == 'Not found.'
