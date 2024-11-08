# Generated by Django 3.2.25 on 2024-11-08 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20241108_1126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(help_text='Выберите авторов книги', to='catalog.Author'),
        ),
    ]
