# Generated by Django 5.1.4 on 2025-03-07 21:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='store',
            name='service_areas',
            field=models.ManyToManyField(blank=True, related_name='serving_stores', to='store.area'),
        ),
        migrations.AddField(
            model_name='area',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='store.province'),
        ),
        migrations.AddField(
            model_name='store',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stores', to='store.province'),
        ),
        migrations.AlterUniqueTogether(
            name='area',
            unique_together={('name', 'province')},
        ),
    ]
