from django.contrib import admin

# Register your models here.
from applications.notifications.models import Contact

admin.site.register(Contact)
