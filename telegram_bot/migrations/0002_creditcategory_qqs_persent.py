# Generated by Django 5.2 on 2025-04-16 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcategory',
            name='qqs_persent',
            field=models.IntegerField(default=0),
        ),
    ]
