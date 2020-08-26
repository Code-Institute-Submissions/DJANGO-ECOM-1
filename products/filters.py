from .models import Product, SubCategory
from django import forms
import django_filters


class ProductFilter(django_filters.FilterSet):
    price_lt = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte')
    subCategory = django_filters.ModelMultipleChoiceFilter(
        queryset=SubCategory.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['image', 'title', 'desc', 'tags', 'price']
