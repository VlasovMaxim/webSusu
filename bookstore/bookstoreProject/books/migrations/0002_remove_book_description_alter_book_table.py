# Generated by Django 5.1.6 on 2025-02-23 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='description',
        ),
        migrations.AlterModelTable(
            name='book',
            table='books',
        ),
    ]
