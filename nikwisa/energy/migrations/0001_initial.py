# Generated by Django 5.1.4 on 2025-02-06 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnergyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('image', models.ImageField(upload_to='category_images/')),
                ('categories', models.ManyToManyField(related_name='energy_categories', to='categories.category')),
            ],
        ),
        migrations.CreateModel(
            name='EnergySubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('categories', models.ManyToManyField(related_name='subcategories', to='energy.energycategory')),
            ],
        ),
    ]
