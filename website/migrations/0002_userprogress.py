# Generated by Django 4.2.7 on 2023-12-03 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProgress",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("current_week", models.IntegerField(blank=True, null=True)),
                ("start_date", models.DateField(blank=True, null=True)),
                (
                    "satisfied_requirements",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "user_progress",
            },
        ),
    ]
