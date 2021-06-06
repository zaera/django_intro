# from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from currency_app.models import Rate


# Create your views here.

def hello_world(request):
    return HttpResponse("""
                        <html>
                        <style>
                            .center {
                            padding: 25% 0;
                            text-align: center;
                            }
                        </style>
                        <div class=center><h3>Hello world!</h3>
                        <p>
                        <h1><label id='loading'></label><h1>
                        </div>
                        </html>
                        <script>
                            var loading = (function() {
                              var h = ['|', '/', '-', ")"];
                              var i = 0;
                              return setInterval(() => {
                                i = (i > 3) ? 0 : i;
                                document.getElementById('loading').innerHTML=h[i];
                                i++;
                              }, 50);
                            })();
                            cosnole.log(1)
                        </script>
                        """)


def index_page(request):
    return HttpResponse("""
                        <html>
                        <style>
                        .center {
                        padding: 25% 0;
                        text-align: center;
                        }
                        </style>
                        <body>
                        <div class=center>
                        <h3>
                        My first page on django. <p><a href="/hello_world">Link to hello world</a>
                        </h3>
                        </div>
                        </body>
                        </html>""")


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
    return HttpResponse('bank_list')


def bank_single(request):
    return HttpResponse('bank_single')


def bank_delete_single(request):
    return HttpResponse('bank_delete_single')
