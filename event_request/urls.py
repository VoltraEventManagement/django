from django.urls import path,include
from . import views


urlpatterns = [
    path('admin/',include('event_request.admin.urls')),
    path('user/',include('event_request.user.urls')),
    
]