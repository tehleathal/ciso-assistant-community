# Generated by Django 5.1.1 on 2024-11-19 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iam', '0009_create_allauth_emailaddress_objects'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='ref_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='reference id'),
        ),
    ]
