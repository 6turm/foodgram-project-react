# Generated by Django 3.2.3 on 2021-09-17 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_remove_recipe_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='color',
            field=models.CharField(default='orange', max_length=50),
        ),
    ]