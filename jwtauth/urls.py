from django.conf.urls import url
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('api/test/', Test.as_view()),
  path('api/gtoken/', GetToken.as_view()),
  # path('api/rtoken/', RefreshToken.as_view()),
]
