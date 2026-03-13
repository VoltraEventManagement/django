from django.shortcuts import render
from ..models import EventRequest
from rest_framework.generics import CreateAPIView,UpdateAPIView,ListAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from ..serializers import RequestSerializer
from ..models import EventRequest
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class CreateProposal(CreateAPIView,UpdateAPIView,RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer
    lookup_field = 'id'
    def get_queryset(self):
        return EventRequest.objects.all().filter(user = self.request.user)

    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        data = serializer.validated_data['speaker']
       
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MyRequests(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    lookup_field = "eventrequest_id"
    def get_queryset(self):
        data = EventRequest.objects.all().filter(user = self.request.user)
        for event in data:
            if event.status == 'new' and timezone.now() - event.created_at>timedelta(days=1):
                event.status = 'reviewing'
                event.save()
        return data


