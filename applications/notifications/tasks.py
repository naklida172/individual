from django.core.mail import send_mail

from applications.notifications.models import Contact
from main.celery import app


from django.core.mail import send_mail

@app.task
def send_post_info(name):
    text = f'{name} сделал новый пост'

    for user in Contact.objects.all():
        send_mail(
            'от пародии инстаграмма',
            text,
            'homewer2016@gmail.com',
            [user.email]
        )
