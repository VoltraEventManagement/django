from ..serializers import RequestSerializer
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from ..models import EventRequest
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from event.models import Event
from django.core.mail import EmailMultiAlternatives
from django_filters.rest_framework import DjangoFilterBackend


class AllRequests(ListAPIView,RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer
    queryset = EventRequest.objects.all()
    lookup_field = id
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']



class ApproveRequest(APIView):
    def post(self,request,id):
        try:
            request = EventRequest.objects.get(eventrequest_id = id)
        except:
            return Response({"error":"that event request is not found"},status = status.HTTP_400_BAD_REQUEST)
        
        request.status = 'approved'
        request.save()
        
        event = Event.objects.create(title = request.name,date = request.event_date,city = request.city,description = request.description,type= request.event_type,category= request.category,target_audience = request.target_audience,venue= request.venue,is_finished = False)
        
        event.event_speakers.set(request.speaker.all())
        
        formatted_date = request.event_date.strftime("%A, %d %B %Y - %I:%M %p")

        subject = "Your Event Request Has Been Approved 🎉"
        from_email = settings.EMAIL_HOST_USER
        to_email = [request.user.email]

        
        text_content = f"""
        Hello {request.user.username},

        Your event request "{request.name}" has been approved.

        Event Date: {formatted_date}

        One of our team members will reach out shortly to coordinate the next steps.

        Voltra Team
        """

       
        html_content = f"""
        <p>Hello <strong>{request.user.username}</strong>,</p>

        <p>Great news! 🎉</p>

        <p>Your event request titled 
        <strong>"{request.name}"</strong> has been approved.</p>

        <p><strong>Event Date:</strong> {formatted_date}</p>

        <p>One of our team will reach out shortly to coordinate the next steps.</p>

        <p>Best regards,<br>
        Voltra Team</p>
        """

        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()
        return Response({"message":"that request is approved"},status = status.HTTP_200_OK)
        

class RejectRequest(APIView):
    def post(self,request,id):
        try:
            request = EventRequest.objects.get(eventrequest_id = id)
        except:
            return Response({"error":"that event request is not found"},status = status.HTTP_400_BAD_REQUEST)
        
        request.status = 'approved'
        request.save()
        return Response({"message":"that request is rejected"},status = status.HTTP_200_OK)
        
