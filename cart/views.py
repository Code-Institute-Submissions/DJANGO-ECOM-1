from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse, HttpResponseRedirect
from django.contrib import messages
from products.models import Product


# Create your views here.
def add_to_cart(request, product_id):
    cart = request.session.get('shopping_cart', {})
    if product_id not in cart:
        product = get_object_or_404(Product, pk=product_id)
        # product is found, add it to the cart
        cart[product_id] = {
            'id': product_id,
            'title': product.title,
            'cost': 99,
            'qty': 1
        }
        # save the cart back to sessions
        request.session['shopping_cart'] = cart

        messages.success(request, "Product has been added to your cart!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        cart[product_id]['qty'] += 1
        request.session['shopping_cart'] = cart
        messages.success(request, "Product has been added to your cart!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def view_cart(request):
    # retrieve the cart
    cart = request.session.get('shopping_cart', {})
    context = {
        'title': 'View Cart',
        'cart': cart
    }

    return render(request, 'cart/view_cart.html', context)


def remove_from_cart(request, product_id):

    # retrieve the cart from session
    cart = request.session.get('shopping_cart', {})

    # if the book is in the cart
    if product_id in cart:
        # remove it from the cart
        del cart[product_id]
        # save back to the session
        request.session['shopping_cart'] = cart
        messages.success(request, "Item removed from cart successfully!")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
