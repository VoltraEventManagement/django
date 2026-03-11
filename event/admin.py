from django.contrib import admin
from .models import Event,EventUser,Speaker,Photo
from event_request.models import EventRequest
# Register your models here.

admin.site.register(EventUser)
admin.site.register(Event)
admin.site.register(Speaker)
admin.site.register(Photo)
admin.site.register(EventRequest)