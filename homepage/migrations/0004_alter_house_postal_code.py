# Generated by Django 3.2.12 on 2022-05-02 14:10

from django.db import migrations
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_auto_20220502_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='postal_code',
            field=localflavor.br.models.BRPostalCodeField(max_length=9),
        ),
    ]
