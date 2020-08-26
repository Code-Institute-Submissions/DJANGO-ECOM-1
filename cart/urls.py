from django.urls import path
import cart.views

urlpatterns = [
    path('add/<product_id>/', cart.views.add_to_cart, name='add_to_cart_url' ),
    path('view/cart/', cart.views.view_cart, name='view_cart_url' ),
    path('remove/<product_id>', cart.views.remove_from_cart, name='remove_from_cart_url' ),
    path('update_quantity/<product_id>', cart.views.update_quantity, name='update_cart_quantity_url'),
]