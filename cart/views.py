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
            'cost': float(product.price),
            'qty': 1,
            'total_cost': float(product.price),
        }
        # save the cart back to sessions
        request.session['shopping_cart'] = cart

        messages.success(request, "Product has been added to your cart!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        cart[product_id]['qty'] = int(cart[product_id]['qty']) + 1
        cart[product_id]['total_cost'] = float(cart[product_id]['total_cost']) + float(cart[product_id]['cost'])
        request.session['shopping_cart'] = cart
        messages.success(request, f"{cart[product_id]['title']} has been added to your cart!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def view_cart(request):
    # retrieve the cart
    cart = request.session.get('shopping_cart', {})
    total = 0
    for k, v in cart.items():
        total += float(v['cost']) * int(v['qty'])

    context = {
        'total': float("{:.2f}".format(total)),
        'title': 'View Cart',
        'cart': cart
    }

    return render(request, 'cart/view_cart.html', context)


def remove_from_cart(request, product_id):

    # retrieve the cart from session
    cart = request.session.get('shopping_cart', {})

    # if the product is in the cart
    if product_id in cart:
        # remove it from the cart
        del cart[product_id]
        # save back to the session
        request.session['shopping_cart'] = cart
        messages.success(request, "Item removed from cart successfully!")

    return redirect(reverse('view_cart_url'))


def update_quantity(request, product_id):
    cart = request.session.get('shopping_cart')
    if product_id in cart:
        cart[product_id]['qty'] = request.POST['qty']
        cart[product_id]['total_cost'] = int(request.POST['qty']) * float(cart[product_id]['cost'])
        request.session['shopping_cart'] = cart
        messages.success(request,
                         f"Quantity for {cart[product_id]['title']} has been changed")

    return redirect(reverse('view_cart_url'))
