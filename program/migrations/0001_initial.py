# Generated by Django 5.0.11 on 2025-02-23 21:51

import django.db.models.deletion
import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("schedule", "0014_use_autofields_for_pk"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "event_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="schedule.event",
                    ),
                ),
            ],
            bases=("schedule.event", models.Model),
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="name")),
                ("slug", models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name="slug")),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="EventTag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content_object", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="program.event")),
                ("tag", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="program.tag")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="event",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="program.EventTag",
                to="program.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
