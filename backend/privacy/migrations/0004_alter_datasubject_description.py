# Generated by Django 5.1.5 on 2025-03-21 11:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("privacy", "0003_remove_processing_labels_processing_filtering_labels"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datasubject",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="Description"),
        ),
    ]
