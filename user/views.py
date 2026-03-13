from django.shortcuts import render,get_object_or_404
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



# Create your views here.
User = get_user_model()

class ActivationAccount(APIView):
    permission_classes = [AllowAny]
    def get(self, request,uid,token):
        try:
            pk = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=pk)
            
            user.is_active = True  
            user.save()          
            return Response({"message": "Account activated"}, status=status.HTTP_200_OK)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)




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