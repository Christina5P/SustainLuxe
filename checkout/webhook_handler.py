from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from decimal import Decimal
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
import json
import time
import stripe


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order},
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL},
        )

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [cust_email])

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}', status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        try:
            intent = event.data.object
            pid = intent.id
            bag = intent.metadata.bag
            save_info = intent.metadata.save_info
            print("save_info: ", save_info)

            stripe_charge = stripe.Charge.retrieve(intent.latest_charge)
            billing_details = stripe_charge.billing_details
            shipping_details = intent.shipping
            print("shipping_details:", shipping_details)
            grand_total = Decimal(stripe_charge.amount) / Decimal('100')

            for field, value in shipping_details.address.items():
                print("field, value: ", field, value)
                if value == "":
                    print("field is empty: ", field)
                    shipping_details.address[field] = None

            profile = None
            username = intent.metadata.username
            print("username: ", username)
            if username != 'AnonymousUser':

                profile = UserProfile.objects.get(user__username=username)
                print('profile', profile.username)
                if save_info:
                    print("Saving info to profile")
                else:
                    print("save_info is False or None")

                    profile.default_phone_number = shipping_details.phone or None
                    profile.default_street_address1 = shipping_details.address.get('line1', None)
                    profile.default_postcode = shipping_details.address.get('postal_code', None)
                    profile.default_town_or_city = shipping_details.address.get('city', None)
                    profile.default_country = shipping_details.address.get('country', None)

                    print("Updating profile with:")
                    print("Phone:", shipping_details.phone)
                    print("Address Line 1:", shipping_details.address.get('line1', None))
                    print("Postal Code:", shipping_details.address.get('postal_code', None))
                    print("City:", shipping_details.address.get('city', None))
                    print("Country:", shipping_details.address.get('country', None))
                    profile.save()
                    print("Profile updated successfully!")
                    print("Intent Metadata:", intent.metadata)

            order_exists = False
            attempt = 1
            while attempt <= 5:
                try:
                    order = Order.objects.get(
                        full_name__iexact=shipping_details.name,
                        email__iexact=billing_details.email,
                        phone_number__iexact=shipping_details.phone,
                        country__iexact=shipping_details.address.country,
                        postcode__iexact=shipping_details.address.postal_code,
                        town_or_city__iexact=shipping_details.address.city,
                        street_address1__iexact=shipping_details.address.line1,
                        grand_total=grand_total,
                        original_bag=bag,
                        stripe_pid=pid,
                    )
                    order_exists = True
                    break
                except Order.DoesNotExist:
                    attempt += 1
                    time.sleep(1)

            if order_exists:
                self._send_confirmation_email(order)
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                    status=200,
                )
            else:
                order = None
                try:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        user_profile=profile,
                        email=billing_details.email,
                        phone_number=shipping_details.phone,
                        country=shipping_details.address.country,
                        postcode=shipping_details.address.postal_code,
                        town_or_city=shipping_details.address.city,
                        street_address1=shipping_details.address.line1,
                        original_bag=bag,
                        stripe_pid=pid,
                    )
                    for item_id, item_data in json.loads(bag).items():
                        product = Product.objects.get(id=item_id)
                        if isinstance(item_data, dict):

                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_data.get('quantity'),
                                product_size=item_data.get('size'),
                            )
                        else:
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_data,
                            )
                        order_line_item.save()

                except Exception as e:
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]} | ERROR: {str(e)}',
                        status=500,
                    )

            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
                status=200,
            )

        except Exception as e:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {e}',
                status=500,
            )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        try:
            return HttpResponse(
                content=f'Webhook received: {event["type"]}', status=200
            )
        except Exception as e:
            return HttpResponse(content=f'Webhook error: {str(e)}', status=500)
