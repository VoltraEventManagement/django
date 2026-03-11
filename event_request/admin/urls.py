from django.urls import path
from . import views


urlpatterns = [
    path('requests/',views.AllRequests.as_view(),name = 'all Event requests for admin'),
    path('request/<int:id>/',views.AllRequests.as_view(),name = 'Event request Details for admin(filters)'),
    path('approve/<int:id>/',views.ApproveRequest.as_view(),name='Approve Event Request'),
    path('reject/<int:id>/',views.RejectRequest.as_view(),name='Reject Event Request'),     

]