from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

from django.db import models

User = get_user_model()


class Contact(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
