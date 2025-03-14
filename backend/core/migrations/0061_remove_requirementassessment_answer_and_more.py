# Generated by Django 5.1.5 on 2025-03-03 10:21

import logging
from django.db import migrations, models, transaction

logger = logging.getLogger(__name__)


def convert_question_to_questions(node_urn, old_data):
    """
    Converts the old question format to the new questions format.
    The old format contains "question" (with question_type and question_choices)
    and "questions" (a list of questions with urn and text).
    
    Handles text and date question types which don't have choices.
    """
    if not old_data:
        return {}

    question_type = old_data.get("question_type")
    choices_texts = old_data.get("question_choices") or []

    # Pre-build choices map for efficiency
    choices_maps = {}
    for idx, choice_text in enumerate(choices_texts):
        choices_maps[idx] = {"urn": f"choice:{idx + 1}", "value": choice_text}

    new_questions = {}
    for q in old_data.get("questions") or []:
        urn = q.get("urn")
        if not urn:
            logger.warning(f"Skipping question with missing URN in node {node_urn}")
            continue

        text = q.get("text")
        
        # Handle different question types
        if question_type in ["text", "date"]:
            # Text and date types don't have choices
            new_questions[urn] = {"type": question_type, "text": text}
        else:
            # For choice-based questions, reference the pre-built choices
            choices = []
            for idx, choice_text in enumerate(choices_texts):
                choice_urn = f"{urn}:choice:{idx + 1}"
                choices.append({"urn": choice_urn, "value": choice_text})

            new_questions[urn] = {"type": question_type, "choices": choices, "text": text}

    return new_questions


@transaction.atomic
def migrate_questions(apps, schema_editor):
    """
    For each instance of Requirementnode, read the old "question" field,
    convert it, and store the result in the new "questions" field.
    """
    Requirementnode = apps.get_model("core", "Requirementnode")
    batch_size = 1000
    nodes_to_update = []

    try:
        # Process nodes in batches for better performance
        for instance in Requirementnode.objects.iterator():
            old_questions = getattr(instance, "question", None)
            if old_questions:
                try:
                    instance.questions = convert_question_to_questions(
                        instance.urn, old_questions
                    )
                    nodes_to_update.append(instance)

                    # Process in batches to reduce database load
                    if len(nodes_to_update) >= batch_size:
                        Requirementnode.objects.bulk_update(
                            nodes_to_update, ["questions"]
                        )
                        nodes_to_update = []
                except Exception as e:
                    logger.error(
                        f"Failed to migrate questions for node {instance.urn}: {str(e)}"
                    )

        # Update any remaining nodes
        if nodes_to_update:
            Requirementnode.objects.bulk_update(nodes_to_update, ["questions"])

    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise


@transaction.atomic
def migrate_answers_format(apps, schema_editor):
    """
    Converts the old 'answer' field format to the new 'answers' format.
    Uses batch processing and more efficient data structures.
    Handles text and date type questions which don't have choices.
    """
    RequirementAssessment = apps.get_model("core", "Requirementassessment")
    RequirementNode = apps.get_model("core", "Requirementnode")

    # Build a complete mapping of node URNs to their question types and choices
    node_questions_map = {}
    try:
        for node in RequirementNode.objects.all():
            if not node.questions:
                continue

            for q_urn, q_data in node.questions.items():
                question_type = q_data.get("type")
                choices = q_data.get("choices", [])
                
                # Create a lookup dictionary for choice values to their URNs
                choice_map = {}
                if choices:
                    for choice in choices:
                        choice_map[choice["value"]] = choice["urn"]
                
                node_questions_map[q_urn] = {
                    "node_urn": node.urn, 
                    "type": question_type,
                    "choices": choice_map
                }

        # Process assessments in batches
        batch_size = 1000
        assessments_to_update = []

        for instance in RequirementAssessment.objects.iterator():
            old_answer_data = getattr(instance, "answer", None)
            new_answers = {}

            if not old_answer_data or not isinstance(old_answer_data, dict):
                continue

            try:
                for question_data in old_answer_data.get("questions", []):
                    question_urn = question_data.get("urn")
                    answer_value = question_data.get("answer")

                    # Skip if missing data or mapping
                    if not question_urn or question_urn not in node_questions_map:
                        continue

                    question_info = node_questions_map[question_urn]
                    question_type = question_info["type"]
                    choices_map = question_info["choices"]

                    # Handle different question types
                    if question_type in ["text", "date"]:
                        # For text and date types, keep the answer value as is
                        new_answers[question_urn] = answer_value
                    else:
                        # Handle single-choice answers
                        if isinstance(answer_value, str):
                            if answer_value in choices_map:
                                new_answers[question_urn] = choices_map[answer_value]
                            else:
                                # Keep free-text answers as they are
                                new_answers[question_urn] = answer_value

                if new_answers:
                    instance.answers = new_answers
                    assessments_to_update.append(instance)

                    # Commit in batches
                    if len(assessments_to_update) >= batch_size:
                        RequirementAssessment.objects.bulk_update(
                            assessments_to_update, ["answers"]
                        )
                        assessments_to_update = []

            except Exception as e:
                logger.error(
                    f"Failed to migrate answers for assessment {instance.id}: {str(e)}"
                )

        # Update any remaining assessments
        if assessments_to_update:
            RequirementAssessment.objects.bulk_update(
                assessments_to_update, ["answers"]
            )

    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise


def reverse_migrations(apps, schema_editor):
    """
    Provides a way to reverse the migrations if needed.
    This is a stub that would need implementation for actual reversal.
    """
    logger.warning("Attempted to reverse a one-way migration - no action taken")


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0060_fix_matrix_json_definition"),
    ]

    operations = [
        migrations.AddField(
            model_name="requirementnode",
            name="questions",
            field=models.JSONField(blank=True, null=True, verbose_name="Questions"),
        ),
        migrations.RunPython(migrate_questions, reverse_migrations),
        migrations.RemoveField(
            model_name="requirementnode",
            name="question",
        ),
        migrations.AddField(
            model_name="requirementassessment",
            name="answers",
            field=models.JSONField(blank=True, null=True, verbose_name="Answers"),
        ),
        migrations.RunPython(migrate_answers_format, reverse_migrations),
        migrations.RemoveField(
            model_name="requirementassessment",
            name="answer",
        ),
    ]
