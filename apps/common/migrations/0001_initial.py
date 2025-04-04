# Generated by Django 5.1.8 on 2025-04-04 13:09

import ckeditor_uploader.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('image', models.ImageField(upload_to='banner/', verbose_name='Image')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Banner URL')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('banner_type', models.CharField(choices=[('banner', 'Banner'), ('advertising', 'Advertising')], default='banner', max_length=40, verbose_name='Banner Type')),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='brand/', verbose_name='Image')),
                ('name', models.CharField(max_length=255, verbose_name='Brand Name')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Brand URL')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order number')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=255, verbose_name='Full Name')),
                ('phone_or_email', models.CharField(max_length=255, verbose_name='Phone or Email')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Message')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('country_name', models.CharField(max_length=255, verbose_name='Country Name')),
                ('region', models.CharField(max_length=255, verbose_name='Region')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/', verbose_name='Image')),
                ('icon', models.ImageField(blank=True, max_length=55, null=True, upload_to='icon/', verbose_name='Icon')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Order')),
                ('top', models.BooleanField(default=True, verbose_name='Top category')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='common.category', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='OnlineUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP Address')),
                ('uuid', models.CharField(max_length=255, null=True, verbose_name='UUID')),
                ('is_authenticated', models.BooleanField(default=False, verbose_name='Authenticated')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Quantity')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='online_users', to='common.category', verbose_name='Online User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='Title')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('price_uzs', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Price in UZS')),
                ('discount', models.PositiveIntegerField(default=0, verbose_name='Discount')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='View Count')),
                ('video_url', models.URLField(blank=True, default='image.jfif', null=True, verbose_name='Video Url')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(default='good', verbose_name='Body')),
                ('on_sale', models.BooleanField(default=True, verbose_name='On Sale')),
                ('is_many', models.BooleanField(default=True, verbose_name='Can you sell more?')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('category', models.ForeignKey(limit_choices_to={'parent_isnull': False}, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='common.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='gallery/', verbose_name='Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='galleries', to='common.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Gallery',
                'verbose_name_plural': 'Galleries',
            },
        ),
        migrations.CreateModel(
            name='ProductCharacteristics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='common.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Characteristic',
                'verbose_name_plural': 'Product Characteristics',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Section Name')),
                ('code', models.CharField(max_length=255, null=True, unique=True, verbose_name='Code')),
                ('products', models.ManyToManyField(blank=True, limit_choices_to={'on_sale': True, 'quantity__gt': 0}, related_name='product_sections', to='common.product')),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
            },
        ),
    ]
