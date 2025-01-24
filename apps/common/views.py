from django.shortcuts import render
from . import serializers
from rest_framework import generics
from . import models


class BannerListAPIView(generics.ListAPIView):
    queryset = models.Banner.objects.filter(banner_type='banner').order_by('order')
    serializer_class = serializers.BannerListSerializers
    pagination_class = None
