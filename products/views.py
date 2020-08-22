from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Product

# Create your views here.


def all_products(request):
    products = Product.objects.all()
    context = {
        'title': 'Products',
        'products': products,
        }
    return render(request, 'products/all_products.html', context)
