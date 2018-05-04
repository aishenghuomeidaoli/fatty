from django.shortcuts import render_to_response


def aqi(request):
    return render_to_response('index.html')


def stock(request):
    return render_to_response('stock.html')
