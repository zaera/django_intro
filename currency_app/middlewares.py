from currency_app.models import Analytics
from currency_app import choices
from django.db.models import F


class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        status_code = getattr(response, 'status_code', None)
        response = self.get_response(request)
        # if response.status_code == 200:
        #     request_method = choices.REQUEST_METHOD_CHOICES_MAPPER[request.method]
        #     obj, created = Analytics.objects.get_or_create(
        #         request_method=request_method, path=request.path,
        #         status_code=status_code,
        #         defaults={'counter': 1}
        #     )
        #     if not created:
        #         Analytics.objects.filter(pk=obj.pk).update(counter=F('counter') + 1, status_code=status_code)

        return response
