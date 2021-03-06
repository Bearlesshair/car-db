# Generated by Django 3.0.2 on 2020-01-06 17:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('make', models.TextField(blank=True, null=True)),
                ('years', models.TextField()),
                ('trims', models.TextField()),
                ('bodystyles', models.TextField()),
                ('url', models.URLField(blank=True, null=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='USD')),
                ('date', models.DateField(default=datetime.date.today)),
                ('city', models.TextField(default='')),
                ('url', models.URLField(blank=True, null=True)),
                ('link', models.URLField()),
                ('stateOrProvince', models.TextField(blank=True, null=True)),
                ('mileage', models.IntegerField(blank=True, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('engine', models.TextField()),
                ('transmission', models.TextField()),
                ('title', models.TextField()),
                ('sellerType', models.TextField()),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='listings', to='cardb.Car')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
