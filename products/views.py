from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from .models import Product, Brand
from .filters import ProductFilter

# Create your views here.


def all_products(request):
    products = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products)
    products = product_filter.qs
    context = {
        'title': 'Products',
        'products': products,
        'product_filter': product_filter,
    }
    return render(request, 'products/all_products.html', context)


def proteins(request):
    brands = Brand.objects.all()
    protein_products = Product.objects.filter(category__title='protein')
    context = {
        'title': 'Protein',
        'products': protein_products,
        'brands': brands,
    }
    return render(request, 'products/category.html', context)


def essentials(request):
    brands = Brand.objects.all()
    essential_products = Product.objects.filter(category__title='essentials')
    context = {
        'title': 'Essentials',
        'products': essential_products,
        'brands': brands,
    }
    return render(request, 'products/category.html', context)


def performance(request):
    brands = Brand.objects.all()
    performance_products = Product.objects.filter(
        category__title='performance')
    context = {
        'title': 'Performance',
        'products': performance_products,
        'brands': brands,
    }
    return render(request, 'products/category.html', context)


def brands(request):
    all_brands = Brand.objects.all()
    context = {
        'title': 'Brands',
        'brands': all_brands,
    }
    return render(request, 'products/brands.html', context)


def search_results(request):
    if 'title' in request.GET and request.GET['title']:
        title = request.GET['title']
        query = Q(title__icontains=title)
    products = Product.objects.filter(query)
    context = {
        'title': 'Search Results',
        'search_term': title,
        'products': products,
    }
    return render(request, 'products/search_result.html', context)


def brand_page(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)
    products = Product.objects.filter(brand__id=brand.id)
    product_filter = ProductFilter(request.GET, queryset=products)
    products = product_filter.qs
    context = {
        'product_filter': product_filter,
        'title': brand.title,
        'brand': brand,
        'products': products
    }
    return render(request, 'products/brand_products.html', context)


def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'title': product.title,
        'product': product
    }
    return render(request, 'products/product_details.html', context)