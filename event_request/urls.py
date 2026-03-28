from django.urls import path,include



urlpatterns = [
    path('admin/',include('event_request.admin.urls')),
    path('user/',include('event_request.user.urls')),
    
]