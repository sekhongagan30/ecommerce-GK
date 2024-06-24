from django.shortcuts import render
from django.template import RequestContext

def handler404(request,exception):
    print("ggn 5", request, exception)
    response = render(request, '404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html')
    response.status_code = 500
    return response

# 403 error