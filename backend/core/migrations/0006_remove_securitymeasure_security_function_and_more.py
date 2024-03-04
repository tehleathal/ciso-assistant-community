# Generated by Django 5.0.2 on 2024-03-04 20:07

import django.db.models.deletion
import iam.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_project_lc_status_alter_securitymeasure_effort'),
        ('iam', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel('SecurityFunction', 'ReferenceControl'),
        migrations.DeleteModel("Policy"),
        migrations.RenameModel('SecurityMeasure', 'AppliedControl'),
    ]
