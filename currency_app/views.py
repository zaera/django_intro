# from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from currency_app.models import Rate
from django import forms


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
    class NameForm(forms.Form):
        your_name = forms.CharField(label='Form', max_length=100)

    queryset = Rate.objects.all()
    ls = []
    for obj in queryset:
        ls.append(obj.sale)
        context = {
            'ls': queryset,
            "form": NameForm(),
        }
    return render(request, 'tmp1.html', context=context)
