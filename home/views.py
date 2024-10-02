from django.shortcuts import render

# Create your views here.


def index(request):
    """ A view to return index page"""

    return render(request, 'home/index.html')


def sell_view(request):
    return render(request, 'sell.html')
