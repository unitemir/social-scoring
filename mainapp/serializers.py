from rest_framework import serializers

from .models import InstagramUser


class CreateInstagramUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstagramUser
        fields = "__all__"
