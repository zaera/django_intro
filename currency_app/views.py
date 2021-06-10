# from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import urllib.parse
from currency_app.models import Rate, Bank, ContactUs
from currency_app.forms import BankForm, ContactUsForm, RateForm


def handler404(request, exception, template_name="index.html"):
    response = render(template_name)
    response.status_code = 404
    return response


def index_page(request):
    if request.method == 'POST':
        form_data = request.POST
        form = ContactUsForm(form_data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    elif request.method == 'GET':
        form = ContactUsForm()
    context = {
        'form': form,
    }
    return render(request, 'index.html', context=context)


def rate_list(request):
    if request.method == 'POST':
        form_data = request.POST
        form = RateForm(form_data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/currency/rate/list/')
    elif request.method == 'GET':
        form = RateForm()
    queryset = Rate.objects.all()
    context = {
        'ls': queryset,
        'form': form,
    }
    return render(request, 'rate_list.html', context=context)


def rate_edit(request, pk, m, s, b, src):
    instance = get_object_or_404(Rate, pk=pk) # noqa
    rate = Rate.objects.get(id=pk)
    rate.moneytype = m
    rate.sale = s
    rate.buy = b
    rate.source = src
    rate.save()
    return HttpResponseRedirect('/currency/rate/list/')


def rate_delete_single(request, pk):
    instance = get_object_or_404(Rate, pk=pk) # noqa
    Rate.objects.filter(id=pk).delete()
    return HttpResponseRedirect('/currency/rate/list/')


def bank_list(request):
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


def bank_delete(request, pk):
    instance = get_object_or_404(Bank, pk=pk) # noqa
    Bank.objects.filter(id=pk).delete()
    return HttpResponseRedirect('/currency/bank/list/')


def contact_us_list(request):
    queryset = ContactUs.objects.all()
    context = {
        'data': queryset,
    }
    return render(request, 'contact_us_list.html', context=context)


def contact_us_delete(request, pk):
    instance = get_object_or_404(ContactUs, pk=pk)  # noqa
    ContactUs.objects.filter(id=pk).delete()
    return HttpResponseRedirect('/currency/сontact_us/list/')
