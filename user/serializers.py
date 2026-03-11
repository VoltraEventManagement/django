from djoser.serializers import UserCreateSerializer
from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "password",
            "role",
            "phone_no",
            "city",
            "user_status",
            
        )

        extra_kwargs = {
            "phone_no": {"required": True},
            "city": {"required": True},
            "password": {"write_only": True},
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','role','id','phone_no','user_status','city','email']
    



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["role"] = user.role
        token["email"] = user.email

        return token
    
