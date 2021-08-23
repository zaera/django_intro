from currency_app.tasks import get_pivdenniy
from currency_app.models import Rate
from unittest.mock import MagicMock


def test_kredo(mocker):
    Rate.objects.all().delete()
    mock_json = lambda: [   # noqa
        ["Долар США", "USD", 26.65, 26.75, 26.6455], ["Євро", "EUR", 31.0, 31.28, 31.2379],  # noqa
        ["Російський рубль", "RUB", 0.34, 0.39, 0.3618],
        ["Швейцарський франк", "CHF", 28.4, 29.7, 29.1224],
        ["Англійський фунт стерлінгів", "GBP", 35.6, 37.6, 36.6762],
        ["Польський злотий", "PLN", 6.5, 6.95, 6.8485]
    ]
    requests_get = mocker.patch('requests.get', return_value=MagicMock(json=mock_json))  # noqa
    initial_count = Rate.objects.count()
    get_pivdenniy()
    assert Rate.objects.count() == initial_count + 2
    get_pivdenniy()
    assert Rate.objects.count() == initial_count + 2
