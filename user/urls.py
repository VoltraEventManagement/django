from django.urls import path,include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from . import views
from . views import ActivationAccount,CustomTokenObtainPairView
urlpatterns = [
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>/', ActivationAccount.as_view(), name='activate_account'),
    path('account/',views.AccountListView.as_view(),name = 'my account'),
    path('update/account/',views.AccountUpdateView.as_view(),name = 'update my account'),
]
# urlpatterns = [
#     path("auth/", include('djoser.urls')),
#     path("auth/", include('djoser.urls.jwt')),
    
# ]
