from rest_framework import serializers
from . import models


class BannerListSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = ('id', 'title', 'image', 'url', 'description')