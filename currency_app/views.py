from django.shortcuts import render
from django.http import HttpResponse


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
                            </html>                                                                                                                   
                        """)
