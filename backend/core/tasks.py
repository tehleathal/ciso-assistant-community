from datetime import date
from huey import crontab
from huey.contrib.djhuey import periodic_task, task, db_periodic_task, db_task
from core.models import AppliedControl
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
import logging
import random
from global_settings.models import GlobalSettings

import logging.config
import structlog

logging.config.dictConfig(settings.LOGGING)
logger = structlog.getLogger(__name__)


# @db_periodic_task(crontab(minute='*/1'))# for testing
@db_periodic_task(crontab(hour="6", minute="0"))
def check_controls_with_expired_eta():
    expired_controls = (
        AppliedControl.objects.exclude(status="active")
        .filter(eta__lt=date.today(), eta__isnull=False)
        .prefetch_related("owner")
    )
    # Group by individual owner
    owner_controls = {}
    for control in expired_controls:
        for owner in control.owner.all():
            if owner.email not in owner_controls:
                owner_controls[owner.email] = []
            owner_controls[owner.email].append(control)
    # Send personalized email to each owner
    for owner_email, controls in owner_controls.items():
        send_notification_email_expired_eta(owner_email, controls)


# @db_periodic_task(crontab(minute='*/1'))# for testing
@db_periodic_task(crontab(hour="5", minute="30"))
def check_deprecated_controls():
    deprecated_controls_list = AppliedControl.objects.filter(status="active").filter(
        expiry_date__lte=date.today(), expiry_date__isnull=False
    )

    deprecated_controls = deprecated_controls_list.prefetch_related("owner")

    # Group by individual owner
    owner_controls = {}
    for control in deprecated_controls:
        for owner in control.owner.all():
            if owner.email not in owner_controls:
                owner_controls[owner.email] = []
            owner_controls[owner.email].append(control)

    # Update the status of each expired control
    deprecated_controls_list.update(status="deprecated")

    for owner_email, controls in owner_controls.items():
        send_notification_email_deprecated_control(owner_email, controls)


@task()
def send_notification_email_expired_eta(owner_email, controls):
    if not check_email_configuration(owner_email, controls):
        return

    subject = f"CISO Assistant: You have {len(controls)} expired control(s)"
    message = "Hello,\n\nThe following controls have expired:\n\n"
    for control in controls:
        message += f"- {control.name} (ETA: {control.eta})\n"
    message += "\nThis reminder will stop once the control is marked as active or you update the ETA.\n"
    message += "Log in to your CISO Assistant portal and check 'my assignments' section to get to your controls directly.\n\n"
    message += "Thank you."

    send_notification_email(subject, message, owner_email)


@task()
def send_notification_email_deprecated_control(owner_email, controls):
    if not check_email_configuration(owner_email, controls):
        return

    subject = f"CISO Assistant: You have {len(controls)} deprecated control(s)"
    message = (
        "Hello,\n\nThe following controls have the expiracy date set to today:\n\n"
    )
    for control in controls:
        message += f"- {control.name} (Set to: deprecated)\n"
    message += "\nThis control(s) will be set to deprecated.\n"
    message += "Log in to your CISO Assistant portal and check 'my assignments' section to get to your controls directly.\n\n"
    message += "Thank you."

    send_notification_email(subject, message, owner_email)


@task()
def send_notification_email(subject, message, owner_email):
    try:
        logger.debug("Sending notification email", subject=subject, message=message)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[owner_email],
            fail_silently=False,
        )
        logger.info(f"Successfully sent notification email to {owner_email}")
    except Exception as e:
        logger.error(f"Failed to send notification email to {owner_email}: {str(e)}")


@task()
def check_email_configuration(owner_email, controls):
    notifications_enable_mailing = GlobalSettings.objects.get(name="general").value.get(
        "notifications_enable_mailing", False
    )
    if not notifications_enable_mailing:
        logger.warning(
            "Email notification is disabled. You can enable it under Extra/Settings. Skipping for now."
        )
        return False

    # Check required email settings
    required_settings = ["EMAIL_HOST", "EMAIL_PORT", "DEFAULT_FROM_EMAIL"]
    missing_settings = [
        setting
        for setting in required_settings
        if not hasattr(settings, setting) or not getattr(settings, setting)
    ]

    if missing_settings:
        error_msg = f"Cannot send email notification: Missing email settings: {', '.join(missing_settings)}"
        logger.error(error_msg)
        return False

    if not owner_email:
        logger.error("Cannot send email notification: No recipient email provided")
        return False

    return True
