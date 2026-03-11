from django.shortcuts import render
from .models import EventRequest
from rest_framework.generics import CreateAPIView,UpdateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RequestSerializer
from .models import EventRequest
from datetime import timedelta
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class CreateProposal(CreateAPIView,UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer
    queryset = EventRequest.objects.all()
    lookup_field = 'id'

class MyRequests(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    def get_queryset(self):
        data = EventRequest.objects.all().filter(user = self.request.user)
        for event in data:
            if event.status == 'new' and timezone.now() - event.created_at>timedelta(days=1):
                event.status = 'reviewing'
                event.save()
        return data
