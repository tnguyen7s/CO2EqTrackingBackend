# Generated by Django 4.0.4 on 2022-06-19 16:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0005_electricity_consumer_flight_consumer_fuel_consumer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='electricity',
            name='month',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='flight',
            name='month',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='fuel',
            name='month',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='meal',
            name='month',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='transport',
            name='month',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)]),
        ),
    ]