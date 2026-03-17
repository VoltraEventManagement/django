from django.shortcuts import render,get_object_or_404,redirect
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.generics import UpdateAPIView,RetrieveAPIView
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseBadRequest
from djoser.email import ActivationEmail
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

# Create your views here.
User = get_user_model()



# ---------------------------
# Activation View
# ---------------------------
def CustomActivate(request, uid, token):
    try:
        uid_decoded = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid_decoded)
    except Exception:
        return HttpResponseBadRequest("Invalid activation link")

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("https://alx-voltra.vercel.app/login")

    return HttpResponseBadRequest("Invalid or expired token")


class AccountListView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)



class AccountUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer