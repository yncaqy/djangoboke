# Generated by Django 4.1.3 on 2022-11-11 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0005_articlepost_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="articlepost",
            name="likes",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
