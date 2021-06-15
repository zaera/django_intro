# from django.shortcuts import render
# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from currency_app.models import Rate, Bank, ContactUs
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from currency_app.forms import BankForm


def handler404(request, exception, template_name="index.html"):
    response = render(template_name)
    response.status_code = 404
    return response


def index_page(request):
    return render(request, 'index.html')


class Ratelist(ListView):
    model = Rate
    fields = (
        'moneytype',
        'sale',
        'buy',
        'source',
    )
    template_name = 'rate_list.html'
    success_url = reverse_lazy('rate-list')


def rate_edit(request, pk, m, s, b, src):
    instance = get_object_or_404(Rate, pk=pk) # noqa
    rate = Rate.objects.get(id=pk)
    rate.moneytype = m
    rate.sale = s
    rate.buy = b
    rate.source = src
    rate.save()
    # return HttpResponseRedirect(reverse('currency_app:rate-list'))
    return redirect('currency_app:rate-list')


def rate_delete_single(request, pk):
    instance = get_object_or_404(Rate, pk=pk) # noqa
    Rate.objects.filter(id=pk).delete()
    # return HttpResponseRedirect(reverse('currency_app:rate-list'))
    return redirect('currency_app:rate-list')


class BankList(ListView):
    model = Bank
    fields = (
        'name',
        'url',
    )
    template_name = 'bank_list.html'
    success_url = reverse_lazy('currency_app:bank-list')


class BankCreate(CreateView):
    model = Bank
    fields = (
        'name',
        'url',
    )
    template_name = 'bank_create.html'
    success_url = reverse_lazy('currency_app:bank-list')


class BankReadSingle(DetailView):
    model = Bank
    template_name = 'bank_read_single.html'
    success_url = reverse_lazy('currency_app:bank-list')


class BankUpdateSingle(UpdateView):
    queryset = Bank.objects.all()
    template_name = 'bank_update_single.html'
    success_url = reverse_lazy('currency_app:bank-list')
    form_class = BankForm


class BankDeleteSingle(DeleteView):
    model = Bank
    queryset = Bank.objects.all()
    template_name = 'bank_delete_single.html'
    success_url = reverse_lazy('currency_app:bank-list')


class ContactUsCreate(CreateView):
    model = ContactUs
    fields = (
        'email_from',
        'subject',
        'message',
    )
    template_name = 'contact_us_create.html'
    success_url = reverse_lazy('index')


def contact_us_list(request):
    queryset = ContactUs.objects.all()
    context = {
        'data': queryset,
    }
    return render(request, 'contact_us_list.html', context=context)


def contact_us_delete(request, pk):
    instance = get_object_or_404(ContactUs, pk=pk)  # noqa
    ContactUs.objects.filter(id=pk).delete()
    # return HttpResponseRedirect(reverse('currency_app:contact_us_list'))
    return redirect('currency_app:contact_us_list')


# html shrinked and resued
#
#
# createview не имеет првоерки на инпут(который был дефолтный при создании формы вручную)?
