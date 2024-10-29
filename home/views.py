from django.shortcuts import render
from django.conf import settings


def index(request):
    """ A view to return index page"""

    return render(request, 'home/index.html')


def sell_view(request):
    return render(request, 'home/sell.html')


def sell_clothes(request):
    cards = [
        {
            'image_url': f'{settings.MEDIA_URL}createaccount.png',
            'title': 'Create Your Account',
            'description': 'Signing up is quick and simple. Just fill out our registration form to get started.',
        },
        {
            'image_url': f'{settings.MEDIA_URL}order.png',
            'title': 'Fill in Your Sale Order',
            'description': 'Submit a sale order for your items and let us handle the rest.',
        },
        {
            'image_url': f'{settings.MEDIA_URL}freightpost.png',
            'title': 'Receive a Freight Post',
            'description': 'Get a freight post to ship your items easily.',
        },
        {
            'image_url': f'{settings.MEDIA_URL}profitsharing.png',
            'title': 'Profit Sharing',
            'description': 'You earn 70% of the sale price and 5% donated to save the earth.',
        },
        {
            'image_url': f'{settings.MEDIA_URL}returnoptions.png',
            'title': 'Flexible Return Options',
            'description': 'Choose to pay for return freight or donate unsold items.',
        },
        {
            'image_url': f'{settings.MEDIA_URL}trackaccount.png',
            'title': 'Track Your Sales',
            'description': 'Monitor your selling progress through your profile.',
        },
    ]

    return render(request, 'home/sell.html', {'cards': cards})
