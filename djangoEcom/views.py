from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from products.models import Product

# Create your views here.


def index(request):
    featured_products = Product.objects.filter(tags__title='featured')
    print(featured_products)
    context = {
        'featured_products': featured_products,
    }
    return render(request, 'index.html', context)