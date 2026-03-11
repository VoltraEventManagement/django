from rest_framework import serializers
from .models import EventUser

class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        fields = '__all__'