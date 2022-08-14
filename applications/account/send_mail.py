from django.core.mail import send_mail


def send_confirmation_email(code, email):
    full_link = f'подобие инстаграмма приветствует ' \
                f' http://localhost:8000/api/v1/account/activate/{code}'

    send_mail(
        'From furniture shop ',
        full_link,
        'homewer2016@gmail.com',
        [email]
    )