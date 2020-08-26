from django.contrib import admin
from .models import Product, Brand, Tag, Category, SubCategory

# Register your models here.
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(SubCategory)
