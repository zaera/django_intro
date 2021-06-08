# from django.shortcuts import render
# from django.http import HttpResponse
from django.shortcuts import render

from currency_app.models import Rate, Bank


def handler404(request, exception, template_name="index.html"):
    response = render(template_name)
    response.status_code = 404
    return response


def index_page(request):
    context = {
        'data': 'data'
    }
    return render(request, 'contact_us.html', context=context)


def rate_list(request):
    queryset = Rate.objects.all()
    context = {
        'ls': queryset,
    }

    return render(request, 'rate_list.html', context=context)


def rate_single(request, pk):
    rate = Rate.objects.get(id=pk)
    context = {
        'single': rate
    }
    return render(request, 'rate_single.html', context=context)


def rate_delete_single(request, pk):
    Rate.objects.filter(id=pk).delete()
    return render(request, 'rate_single_delete.html')


def bank_list(request):
    queryset = Bank.objects.all()
    context = {
        'ls': queryset,
    }
    return render(request, 'bank_list.html', context=context)


def bank_single(request, pk):
    bank = Bank.objects.get(id=pk)
    context = {
        'single': bank
    }
    return render(request, 'bank_single.html', context=context)


def bank_delete_single(request, pk):
    Bank.objects.filter(id=pk).delete()
    return render(request, 'bank_single_delete.html')
