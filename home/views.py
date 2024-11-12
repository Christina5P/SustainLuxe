from django.shortcuts import render
from django.conf import settings


def index(request):
    """ A view to return index page"""

    return render(request, 'home/index.html')


def sell_view(request):
    return render(request, 'home/sell.html')


def sustainable_view(request):
    return render(request, 'home/sustainable.html')


def sell_clothes(request):
    cards = [
        {
            'image_url': f'{settings.MEDIA_URL}createaccount.png',
            'title': 'Create Your Account',
            'description': 'Signing up is quick and simple. Just fill out our registration form to get started.',
            'long_description': """Setting up an account is essential to ensure you can securely track your profits and access other important features. With your account, you’ll be able to:

            Track Your Earnings: View your current balance and all earnings from items you've sold. This way, you’ll always know exactly how much you’ve earned.

            Request Withdrawals Anytime: Once you have earnings in your account, you’re free to request a withdrawal at any time. The funds will be transferred to your preferred account securely.

            Monitor Your Product Status: Get real-time updates on each product you've listed with us. You’ll know if items are active, pending, or sold.

            Access Your Transaction History: Keep a full record of all withdrawals you've made, so you can stay organized and easily review your earnings.

            Review Your Order History: Access past and current orders so you always have a record of items listed, sold, and earnings made.

            Having an account helps ensure a smooth and transparent experience while selling your products with us. It’s the first step to staying organized and in control of your sales journey!""",
        },
        {
            'image_url': f'{settings.MEDIA_URL}order.png',
            'title': 'Fill in Your Sale Order',
            'description': 'Submit a sale order for your items and let us handle the rest.',
            'long_description': """Completing a sale order for each product allows us to effectively list your items, showcasing their environmental impact and unique features. Here’s what to expect and include:

            Product Details: Fill in the product description thoroughly. Share anything unique or interesting about the item that would appeal to potential buyers—such as the brand, age, condition, or special features.

            Fabric and Weight: Including details like fabric type and weight enables us to calculate the carbon savings from purchasing this item secondhand. This information supports sustainable shopping by helping buyers see the positive environmental impact of their choices.

            Professional Photos and Listing: After we receive your product, our team will add professional images and any other necessary details. Once everything is set, we’ll list your item in our online shop for up to 3 months.

            Product Expiry and Donation Option: If your item doesn’t sell within 3 months, it can be donated to assist those in need. If you’d prefer to have the item returned to you instead, simply check the box in the form. You’ll need to cover the return shipping cost if this option is selected.

            Completing the form accurately and providing a compelling description will help your item attract the right buyers.!""",
        },
        {
            'image_url': f'{settings.MEDIA_URL}freightpost.png',
            'title': 'Receive a Freight Post',
            'description': 'Get a freight post to ship your items easily.',
            'long_description': """Once you’ve completed the sell form and received confirmation, we’ll handle the logistics to make it easy for you to send in your product:

            Confirmation of Your Sell Order: Shortly after submitting, you’ll receive an email confirmation that your sale order was successfully created. This lets you know that we’re ready to receive your item.

            Shipping Bag and Free Freight Ticket: We’ll mail you a shipping bag along with a prepaid freight ticket—no cost to you! This package includes everything you need to securely pack and send your item.

            Simple Shipping Process: Pack your item carefully in the bag provided, attach the freight ticket, and drop it off at the specified carrier. Once we receive your item, our team will handle the rest: preparing it for listing, photographing it, and adding any final details to get it ready for sale.

            This easy, free shipping service is designed to make the process as smooth as possible, so you can focus on clearing space and earning from your items without the hassle of shipping costs.""",
        },
        {
            'image_url': f'{settings.MEDIA_URL}profitsharing.png',
            'title': 'Profit Sharing',
            'description': 'You earn 70% of the sale price and 5% donated to save the earth.',
            'long_description': """When selling with us, you have full control over pricing and can feel good about the positive impact of your sale:

Set Your Price, Earn 70% Profit: You choose the price for your item, and we ensure you receive 70% of that amount after the sale. This means you’re directly rewarded for your item’s value, while also sharing in our mission to promote sustainability.

Effortless Donation to Environmental Causes: In addition to your earnings, 5% of the sale price goes toward supporting environmental initiatives. We manage this donation process on your behalf, making it simple to give back. For more information on how your donation makes a difference, please visit our "Sustainable Impact" page.

Sustainable Business Model: Our platform retains 25% of the sale price, which covers administrative costs, shipping logistics, and other operational expenses. This transparent profit-sharing model allows us to maintain a high level of service while prioritizing both your profit and environmental impact.

Selling with us not only earns you money but also contributes to a better world. It’s a simple, rewarding way to make a difference with your pre-loved items.""",
        },
        {
            'image_url': f'{settings.MEDIA_URL}returnoptions.png',
            'title': 'Flexible Return Options',
            'description': 'Choose to pay for return freight or donate unsold items.',
            'long_description': """Our goal is to make selling as convenient and rewarding as possible, which includes offering flexible options for what happens if an item doesn’t sell. Here’s how it works:

            Choose What Happens with Unsold Items: If an item remains unsold after three months, you have two options:

            Return to You: For a small return shipping fee, we’ll send your item back to you. This option ensures that nothing goes to waste and lets you keep or try other ways to sell it.
            Donate to a Good Cause: If you choose not to retrieve the item, we’ll gladly handle the donation process for you. Your unsold items can go on to support individuals in need, offering an environmentally friendly and impactful way to give back.
            Simple Process and Transparent Tracking: Regardless of your choice, you can track the status of each item through your account, where you’ll receive updates about which items are up for sale, which have sold, and the status of any items waiting for a final decision.

            A Sustainable and Stress-Free Approach: We believe in making it easy for you to do good while selling your items. Our return and donation options are designed to reduce waste and promote sustainability, ensuring that your items continue to have value—either as returned possessions or as donations that make a positive impact.

            Selling with us means you’re part of a meaningful cycle, one where your items either find new homes or go on to help those in need. It’s one more way we’re working together for a better future.""",
        },
        {
            'image_url': f'{settings.MEDIA_URL}trackaccount.png',
            'title': 'Track Your Sales',
            'description': 'Monitor your selling progress through your profile.',
            'long_description': """Once you submit the selling form, your account dashboard provides complete visibility over your products and sales. Here's how it works:

            Instant Updates on Your Product: Right after you submit the form, your item will appear in your account, allowing you to monitor its journey from the very beginning.

            Product Status Tracking: Through your account, you can keep tabs on every aspect of your listed items:

            Listed and Available: View when each product becomes available in the shop.
            Days to Expiration: Monitor the countdown for each item, with reminders about when an unsold item may be donated or returned, based on your preferences.
            Sold Products and Balance Updates: As soon as an item sells, your balance will reflect your earnings, showing you exactly how much you've made from each sale.
            Seamless Withdrawals: Your earnings are always accessible. With our withdrawal menu, you can transfer your balance whenever you choose. Just request a withdrawal, and your funds will be sent to your preferred account quickly and securely.

            By keeping everything organized and transparent, we give you full control over your sales journey. It's a streamlined, worry-free way to turn your items into profit while maintaining visibility every step of the way.""",
        },
    ]

    return render(request, 'home/sell.html', {'cards': cards})
