from django.contrib import admin

# Register your models here.
from applications.account.models import CustomUser

admin.site.register(CustomUser)
