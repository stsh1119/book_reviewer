from flask_mail import Mail, Message
from .celery_creator import celery

mail = Mail()


@celery.task()
def send_notification_email(users_list: list, review_category: str):
    """Sends an email to a list of users, subscribed to some fork category."""
    for user in users_list:
        msg = Message('New review added!',
                      sender='shulga.s1337@gmail.com',
                      recipients=user.split())
        msg.body = f"""Hello, {user},
New book review was added to {review_category}
"""
    mail.send(msg)
