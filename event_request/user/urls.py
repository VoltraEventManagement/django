from django.urls import path,include
from . import views


urlpatterns = [
    path('request/',views.CreateProposal.as_view(),name='create Event Request'),
    path('request/<int:id>/',views.CreateProposal.as_view(),name='update Event Request'),
    path('requests/',views.MyRequests.as_view(),name = "user's event requests(filters applied)"),
   
]