# Generated by Django 5.0.8 on 2024-10-30 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="tour",
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]