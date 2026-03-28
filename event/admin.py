from django.contrib import admin
from .models import Event,EventUser,Speaker,Photo
from event_request.models import EventRequest
# Register your models here.



@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'event_type', 'status', 'event_date', 'city', 'user', 'created_at')
    list_filter  = ('status', 'category', 'event_type', 'city')
    search_fields = ('name', 'user__email', 'city')
    ordering = ('-created_at',)

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'position')
    search_fields = ('name', 'position')
    ordering = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'category', 'date', 'city', 'venue', 'is_finished', 'created_at')
    list_filter  = ('type', 'category', 'venue', 'is_finished', 'city')
    search_fields = ('title', 'city', 'target_audience')
    ordering = ('-created_at',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('photo_id', 'event_id')
    ordering = ('event_id',)


@admin.register(EventUser)
class EventUserAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'user_id', 'get_track', 'is_checked')
    list_filter  = ('is_checked', 'user_id__track')
    search_fields = ('user_id__email', 'user_id__track')
    ordering = ('event_id',)

    def get_track(self, obj):
        return obj.user_id.track
    get_track.short_description = 'Track'
    get_track.admin_order_field = 'user_id__track'