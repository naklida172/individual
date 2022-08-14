from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from applications.notifications.models import Contact
from applications.notifications.permissions import CustomIsAdmin
from applications.notifications.serializers import ContactSerializer


class ContactView(ViewSet):
    query_set = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [CustomIsAdmin]