from djoser.serializers import UserCreateSerializer
from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.email import ActivationEmail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from djoser import conf
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

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
        read_only_fields = ['id', 'role']
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["role"] = user.role
        token["email"] = user.email

        return token
    



class CustomActivationEmail(ActivationEmail):

    def send(self, to=None, *args, **kwargs):
        user = self.context.get("user")
        if not user:
            raise ValueError("CustomActivationEmail requires 'user' in context")

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        
        activation_url = f"https://django-kf3s.vercel.app/api/activate/{uid}/{token}/"
        subject = "Activate your account "

        html_content = f"""
<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; background-color:#f4f4f4; font-family:Arial, sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="padding:20px; background:#f4f4f4;">
<tr><td align="center">
<table width="500" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:10px; padding:30px; text-align:center;">
    <tr><td><h2 style="color:#002b56;">Welcome to <span style="color:#002b56;">Voltra</span> 🚀</h2></td></tr>
    <tr><td>
        <p style="color:#555;">Hi {user.username},</p>
        <p style="color:#555;">You're one step away from getting started. Click the button below to activate your account.</p>
    </td></tr>
    <tr><td style="padding:20px;">
        <a href="{activation_url}"
           style="background:#002b56; color:#ffffff; padding:12px 25px; text-decoration:none; border-radius:5px; display:inline-block;">
           Activate Account
        </a>
    </td></tr>
    <tr><td>
        <p style="color:#999; font-size:13px;">This link will expire soon for security reasons.</p>
        <p style="color:#bbb; font-size:12px;">If you didn't create this account, just ignore this email.</p>
    </td></tr>
    <tr><td style="padding-top:20px; border-top:1px solid #002b56;">
        <p style="color:#002b56; font-size:12px;">© 2026 Voltra. All rights reserved.</p>
    </td></tr>
</table>
</td></tr>
</table>
</body>
</html>
"""

        text_content = f"Hi {user.username}, activate your account: {activation_url}"

        recipient = to if isinstance(to, list) else [to or user.email]

        email = EmailMultiAlternatives(
    subject=subject,
        body=text_content,
        to=recipient
    )
        email.attach_alternative(html_content, "text/html")
        email.send()
