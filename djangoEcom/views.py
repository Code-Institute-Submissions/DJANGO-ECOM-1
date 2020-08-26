from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
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


def search_products(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(title__icontains=request.GET.get('term'))
        titles = []
        for product in qs:
            titles.append(product.title)
        return JsonResponse(titles, safe=False)
