from djoser.serializers import UserCreateSerializer
from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.email import ActivationEmail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from djoser import conf

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
    template_name = None  

    def send(self, to=None, *args, **kwargs):
        user = self.context.get("user")
        if not user:
            raise ValueError("CustomActivationEmail requires 'user' in context")

        
        activation_url_template = settings.DJOSER.get("ACTIVATION_URL") 
        if not activation_url_template:
            raise ValueError("ACTIVATION_URL not defined in DJOSER settings")

        
        uid = self.context.get("uid")
        token = self.context.get("token")
        activation_url = activation_url_template.format(uid=uid, token=token)

        subject = "Activate your account"
        text_content = f"Hello {user.username}, activate your account: {activation_url}"
        html_content = f"""
        <html>
            <body>
                <h2>Hello {user.username}!</h2>
                <p>Click the button below to activate your account:</p>
                <a href="{activation_url}" style="
                    display:inline-block;
                    padding:10px 20px;
                    background-color:#007bff;
                    color:#fff;
                    text-decoration:none;
                    border-radius:5px;
                ">Activate Account</a>
            </body>
        </html>
        """

        msg = EmailMultiAlternatives(subject, text_content, "no-reply@example.com", [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()