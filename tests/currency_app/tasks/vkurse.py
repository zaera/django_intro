from currency_app.tasks import get_vkurse
from currency_app.models import Rate
from unittest.mock import MagicMock


def test_vkurse(mocker):
    Rate.objects.all().delete()
    mock_json = lambda: { # noqa
        "Dollar": {
            "buy": "26.70",
            "sale": "26.85"
        },
        "Euro": {
            "buy": "31.15",
            "sale": "31.30"
        },
        "Rub": {
            "buy": "0.359",
            "sale": "0.363"
        }
    }
    requests_get = mocker.patch('requests.get', return_value=MagicMock(json=mock_json))  # noqa
    initial_count = Rate.objects.count()
    get_vkurse()
    assert Rate.objects.count() == initial_count + 2
    get_vkurse()
    assert Rate.objects.count() == initial_count + 2
