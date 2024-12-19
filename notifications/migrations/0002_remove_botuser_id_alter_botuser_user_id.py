# Generated by Django 5.1.3 on 2024-12-03 16:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="botuser",
            name="id",
        ),
        migrations.AlterField(
            model_name="botuser",
            name="user_id",
            field=models.IntegerField(
                primary_key=True, serialize=False, verbose_name="User ID"
            ),
        ),
    ]