from .models import EventRequest
from rest_framework import serializers
from event.models import Event,Speaker
from django.utils import timezone


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['name','position','linked_profile'] 


class RequestSerializer(serializers.ModelSerializer):
    speaker = SpeakerSerializer(many=True)

    class Meta:
        model = EventRequest
        fields = ['eventrequest_id','name','description','category','event_type','objective','target_audience','expected_attendees','event_date','event_time','city','status','venue','created_at','speaker','paid']

    def validate(self, data):
        
        event_date = data.get('event_date')
        if event_date and event_date < timezone.now().date():
            raise serializers.ValidationError({"event_date": "Event date cannot be in the past."})
        
        for key, value in data.items():
            if isinstance(value, str) and not value.strip():
                raise serializers.ValidationError({key: "This field cannot be empty."})
                
        return data

    def create(self, validated_data):
        speakers_data = validated_data.pop('speaker')
        event = EventRequest.objects.create(user = self.context['request'].user,**validated_data)

        for speaker_data in speakers_data:
            speaker = Speaker.objects.create(**speaker_data)
            event.speaker.add(speaker)

        return event
    
    def update(self, instance, validated_data):
        speakers_data = validated_data.pop('speaker', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if speakers_data is not None:
            instance.speaker.clear()
            for speaker_data in speakers_data:
                speaker = Speaker.objects.create(**speaker_data)
                instance.speaker.add(speaker)
                
        return instance
