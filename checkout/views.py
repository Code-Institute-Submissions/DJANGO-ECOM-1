from django.shortcuts import render, reverse, HttpResponse, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Purchase
from django.contrib import messages
from django.contrib.auth.models import User

# import settings so that we can access the public stripe key
from django.conf import settings
import stripe

from products.models import Product
from django.contrib.sites.models import Site

endpoint_secret = "whsec_xYipceqj7ue6NjYrxnUA3BOAGOa1BOaQ"


def checkout_success(request):
    # Empty the shopping cart
    request.session['shopping_cart'] = {}
    messages.success(request, 'Your purchase has been completed')
    return redirect(reverse('homepage_url'))


def checkout_cancelled(request):
    return HttpResponse('checkout cancelled')


def checkout(request):
    # tell Stripe what my api_key is
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # retrieve my shopping cart
    cart = request.session.get('shopping_cart', {})

    # create our line items
    line_items = []
    all_product_ids = []

    # go through each product in the shopping cart
    for product_id, product in cart.items():
        # retrieve the product by its id from the database
        product_model = get_object_or_404(Product, pk=product_id)

        # create line item
        # you see all the possible properties of a line item at:
        # https://stripe.com/docs/api/invoices/line_item
        item = {
            "name": product_model.title,
            "amount": int(product_model.price * 100),
            "quantity": product['qty'],
            "currency": "usd",
        }

        line_items.append(item)
        all_product_ids.append(str(product_model.id))

    # get the current website
    current_site = Site.objects.get_current()

    # get the domain name
    domain = current_site.domain

    # create a payment session to represent the current transaction
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        client_reference_id=request.user.id,
        metadata={
            "all_book_ids": ",".join(all_product_ids)
        },
        mode="payment",  # take credit cards
        line_items=line_items,
        success_url=domain + reverse('checkout_success'),
        cancel_url=domain + reverse('checkout_cancelled')
    )

    return render(request, "checkout/checkout.html", {
        "session_id": session.id,
        "public_key": settings.STRIPE_PUBLISHABLE_KEY
    })


@csrf_exempt
def payment_completed(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        handle_payment(session)

    return HttpResponse(status=200)


def handle_payment(session):
    # print(session)
    user = get_object_or_404(User, pk=session["client_reference_id"])

    # change the metadata from string back to array
    all_product_ids = session["metadata"]["all_product_ids"].split(",")

    # go through each product id
    for product_id in all_product_ids:
        product_model = get_object_or_404(Product, pk=product_id)

        # create the purchase model
        purchase = Purchase()
        purchase.product_id = product_model
        purchase.user_id = user
        purchase.save()
