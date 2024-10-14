# Generated by Django 5.1 on 2024-10-04 08:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0029_alter_appliedcontrol_link_alter_evidence_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="appliedcontrol",
            name="start_date",
            field=models.DateField(
                blank=True,
                help_text="Start date (useful for timeline)",
                null=True,
                verbose_name="Start date",
            ),
        ),
    ]
