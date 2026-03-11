from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import EventUser
from .serializers import EventUserSerializer
# Create your views here.



class RegisteredEvents(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventUserSerializer
    def get_queryset(self):
        return EventUser.objects.filter(eventuser_id = self.request.user.id)
