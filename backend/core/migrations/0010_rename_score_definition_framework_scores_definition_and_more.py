# Generated by Django 5.0.4 on 2024-04-28 15:34
# well-known scores added manually

from django.db import migrations, models


WELL_KNOWN_SCORES = {
    "urn:intuitem:risk:framework:tisax-v6.0.2": (0, 5),
    "urn:intuitem:risk:framework:ccb-cff-2023-03-01": (1, 5),
    "urn:intuitem:risk:framework:nist-csf-2.0": (1, 4),
}


def fix_well_known_scores(apps, schema_editor):
    Framework = apps.get_model("core", "Framework")
    ComplianceAssessment = apps.get_model("core", "ComplianceAssessment")
    for framework in Framework.objects.all():
        if framework.urn in WELL_KNOWN_SCORES:
            (framework.min_score, framework.max_score) = WELL_KNOWN_SCORES[
                framework.urn
            ]
            framework.save()
            print("custom migration for", framework.urn)
    for assessment in ComplianceAssessment.objects.all():
        if assessment.framework.urn in WELL_KNOWN_SCORES:
            (assessment.min_score, assessment.max_score) = WELL_KNOWN_SCORES[
                assessment.framework.urn
            ]
            print("custom migration for", assessment.framework.urn)
        else:
            # no default value, so fix it now
            (assessment.min_score, assessment.max_score) = (0, 100)
        assessment.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_framework_max_score_framework_min_score_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="framework",
            old_name="score_definition",
            new_name="scores_definition",
        ),
        migrations.RemoveField(
            model_name="requirementnode",
            name="level",
        ),
        migrations.RemoveField(
            model_name="requirementnode",
            name="maturity",
        ),
        migrations.AddField(
            model_name="complianceassessment",
            name="max_score",
            field=models.IntegerField(null=True, verbose_name="Maximum score"),
        ),
        migrations.AddField(
            model_name="complianceassessment",
            name="min_score",
            field=models.IntegerField(null=True, verbose_name="Minimum score"),
        ),
        migrations.AddField(
            model_name="complianceassessment",
            name="scores_definition",
            field=models.JSONField(
                blank=True, null=True, verbose_name="Score definition"
            ),
        ),
        migrations.AddField(
            model_name="complianceassessment",
            name="selected_implementation_groups",
            field=models.JSONField(
                blank=True, null=True, verbose_name="Selected implementation groups"
            ),
        ),
        migrations.AddField(
            model_name="framework",
            name="implementation_groups_definition",
            field=models.JSONField(
                blank=True, null=True, verbose_name="Implementation groups definition"
            ),
        ),
        migrations.AddField(
            model_name="requirementassessment",
            name="selected",
            field=models.BooleanField(default=True, verbose_name="Selected"),
        ),
        migrations.AddField(
            model_name="requirementnode",
            name="implementation_groups",
            field=models.JSONField(null=True, verbose_name="Implementation groups"),
        ),
        migrations.DeleteModel(
            name="RequirementLevel",
        ),
        migrations.RunPython(fix_well_known_scores),
    ]
