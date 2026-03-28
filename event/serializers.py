from rest_framework import serializers
from .models import EventUser,Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventUserSerializer(serializers.ModelSerializer):
    event_id = EventSerializer()
    class Meta:
        model = EventUser
        fields = '__all__'
