from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/obtain', TokenObtainPairView.as_view(), name="obtaintoken"),
    path('token/refresh', TokenRefreshView.as_view(), name="refreshtoken")
]
