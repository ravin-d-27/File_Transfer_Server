# Generated by Django 4.2.7 on 2023-12-21 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
