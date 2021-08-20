from currency_app.tasks import get_pb
from currency_app.models import Rate
from unittest.mock import MagicMock


def test_pb(mocker):
    Rate.objects.all().delete()
    mock_json = lambda: [   # noqa
        {"ccy": "USD", "base_ccy": "UAH", "buy": "26.45000", "sale": "26.85000"},
        {"ccy": "EUR", "base_ccy": "UAH", "buy": "30.90000", "sale": "31.50000"},
        {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.34800", "sale": "0.37800"},
        {"ccy": "BTC", "base_ccy": "USD", "buy": "44910.0594", "sale": "49637.4340"}
    ]
    requests_get = mocker.patch('requests.get', return_value=MagicMock(json=mock_json)) # noqa
    initial_count = Rate.objects.count()
    get_pb()
    assert Rate.objects.count() == initial_count + 2
    get_pb()
    assert Rate.objects.count() == initial_count + 2
