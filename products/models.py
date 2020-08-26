from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class Brand(models.Model):
    title = models.CharField(blank=False, max_length=50)
    desc = models.TextField(blank=False)
    image = CloudinaryField(blank=True, null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(blank=False, max_length=50)
    desc = models.TextField(blank=False)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(blank=False, max_length=50)

    # relationships
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(blank=False, max_length=100)
    desc = models.TextField(blank=False)
    image = CloudinaryField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)

    # relationships
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subCategory = models.ManyToManyField(SubCategory, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
