from django.urls import path,include
from . import views
urlpatterns = [
    path('myEvents/',views.RegisteredEvents.as_view(),name="my registered events"),
    
]