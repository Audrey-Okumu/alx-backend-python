#Register models for testing in the admin panel.

from django.contrib import admin
from .models import Message, Notification

admin.site.register(Message)
admin.site.register(Notification)
