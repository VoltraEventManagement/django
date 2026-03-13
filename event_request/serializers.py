from .models import EventRequest
from rest_framework import serializers
from event.models import Event,Speaker



class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['name','position'] 


class RequestSerializer(serializers.ModelSerializer):
    speaker = SpeakerSerializer(many=True)

    class Meta:
        model = EventRequest
        fields = ['id','name','description','category','event_type','objective','target_audience','expected_attendees','event_date','city','status','venue','created_at','speaker']


    def create(self, validated_data):
        speakers_data = validated_data.pop('speaker')
        event = EventRequest.objects.create(user = self.context['request'].user,**validated_data)

        for speaker_data in speakers_data:
            speaker = Speaker.objects.create(**speaker_data)
            event.speaker.add(speaker)

        return event
    
