from django.db import models

# Create your models here.


class Brand(models.Model):
    title = models.CharField(blank=False, max_length=50)
    desc = models.TextField(blank=False)

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


class Product(models.Model):
    title = models.CharField(blank=False, max_length=100)
    desc = models.TextField(blank=False)

    # relationships
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
