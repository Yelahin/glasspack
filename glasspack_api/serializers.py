from django.contrib.auth import get_user_model
from rest_framework import serializers
from glasspack_site.models import Product
from glasspack_users.models import UserMessage


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["time_create"]


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = ['full_name', 'email', 'comment']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'], 
            password=validated_data['password']
        )
        return user
