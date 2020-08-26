def cart_contents(request):
    # make the content of the shopping cart available to all templates
    cart = request.session.get("shopping_cart", {})
    number_of_items = 0
    for k, v in cart.items():
        number_of_items += int(v['qty'])
    return {
        'shopping_cart': cart,
        'number_of_items': number_of_items,
    }
