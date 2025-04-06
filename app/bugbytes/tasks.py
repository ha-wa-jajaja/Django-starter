from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_order_confirmation_email(order_id, user_email):
    """
    A Celery task to send an email.

    Args:
        subject (str): The subject of the email.
        message (str): The body of the email.
        recipient_list (list): A list of recipient email addresses.
    """
    subject = f"Order Confirmation - {order_id}"
    message = f"Your order with ID {order_id} has been confirmed."
    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )
