# from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import urllib.parse

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
    instance = get_object_or_404(Rate, pk=pk) # noqa
    rate = Rate.objects.get(id=pk)
    context = {
        'single': rate
    }
    return render(request, 'rate_single.html', context=context)


def rate_delete_single(request, pk):
    instance = get_object_or_404(Rate, pk=pk) # noqa
    Rate.objects.filter(id=pk).delete()
    return render(request, 'rate_single_delete.html')


def bank_list(request):
    from currency_app.forms import BankForm

    if request.method == 'POST':
        form_data = request.POST
        form = BankForm(form_data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/currency/bank/list/')
    elif request.method == 'GET':
        form = BankForm()
    queryset = Bank.objects.all()
    context = {
        'ls': queryset,
        'form': form,
    }
    return render(request, 'bank_list.html', context=context)


def bank_edit(request, pk, npk, upk):
    instance = get_object_or_404(Bank, pk=pk) # noqa
    bank = Bank.objects.get(id=pk)
    bank.name = npk
    bank.url = urllib.parse.unquote(upk)
    bank.save()
    return HttpResponseRedirect('/currency/bank/list/')


def bank_delete_single(request, pk):
    instance = get_object_or_404(Bank, pk=pk) # noqa
    Bank.objects.filter(id=pk).delete()
    return HttpResponseRedirect('/currency/bank/list/')
