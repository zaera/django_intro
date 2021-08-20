from currency_app.tasks import get_abank
from currency_app.models import Rate
from unittest.mock import MagicMock


def test_abank(mocker):
    Rate.objects.all().delete()
    mock_json = lambda: {   # noqa
        "data": [{"rateA": 1, "rateB": 26.55, "ccyA": "USD", "ccyB": "UAH"},
                 {"rateA": 26.8, "rateB": 1, "ccyA": "UAH", "ccyB": "USD"},
                 {"rateA": 1, "rateB": 30.9, "ccyA": "EUR", "ccyB": "UAH"},
                 {"rateA": 31.3, "rateB": 1, "ccyA": "UAH", "ccyB": "EUR"}],
        "processing": [{"rateA": 1, "rateB": 26.5, "ccyA": "USD", "ccyB": "UAH"},
                       {"rateA": 26.7379, "rateB": 1, "ccyA": "UAH", "ccyB": "USD"},
                       {"rateA": 1, "rateB": 30.9, "ccyA": "EUR", "ccyB": "UAH"},
                       {"rateA": 31.25, "rateB": 1, "ccyA": "UAH", "ccyB": "EUR"},
                       {"rateA": 1, "rateB": 0.355, "ccyA": "RUB", "ccyB": "UAH"},
                       {"rateA": 0.375, "rateB": 1, "ccyA": "UAH", "ccyB": "RUB"}],
        "nbu": [{"rateA": 1, "rateB": 0.35951, "ccyA": "RUB", "ccyB": "UAH"},
                {"rateA": 0.35951, "rateB": 1, "ccyA": "UAH", "ccyB": "RUB"},
                {"rateA": 1, "rateB": 26.6504, "ccyA": "USD", "ccyB": "UAH"},
                {"rateA": 26.6504, "rateB": 1, "ccyA": "UAH", "ccyB": "USD"},
                {"rateA": 1, "rateB": 31.169, "ccyA": "EUR", "ccyB": "UAH"},
                {"rateA": 31.169, "rateB": 1, "ccyA": "UAH", "ccyB": "EUR"}],
        "date": "2021-08-20 03:52:01", "status": "ok", "result": "ok",
        "timestamp": "2021-08-20 03:56:40", "request_ref": "", "response_ref": "611efdc89ac4f"
    }
    requests_get = mocker.patch('requests.get', return_value=MagicMock(json=mock_json))  # noqa
    initial_count = Rate.objects.count()
    get_abank()
    assert Rate.objects.count() == initial_count + 2
    get_abank()
    assert Rate.objects.count() == initial_count + 2
