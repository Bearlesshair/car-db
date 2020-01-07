# Generated by Django 3.0.2 on 2020-01-06 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='bodystyles',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='make',
            field=models.TextField(default='No Make'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='car',
            name='trims',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='years',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='engine',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=15, verbose_name='USD'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listing',
            name='sellerType',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='transmission',
            field=models.TextField(blank=True, null=True),
        ),
    ]