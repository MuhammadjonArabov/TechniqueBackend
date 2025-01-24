from django.urls import path
from . import views

urlpatterns = [
    path('banners/', views.BannerListAPIView.as_view(), name='banner-list')
]