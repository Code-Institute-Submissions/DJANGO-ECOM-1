# Generated by Django 2.2.6 on 2020-08-25 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_brand_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='subCategory',
            field=models.ManyToManyField(blank=True, to='products.SubCategory'),
        ),
    ]
