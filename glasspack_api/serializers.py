from django.contrib.auth import get_user_model
from rest_framework import serializers
from glasspack_site.models import Product
from glasspack_users.models import UserMessage


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["time_create"]


class ProductCountSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    count = serializers.IntegerField()


class SelectedFiltersSerializer(serializers.Serializer):
    selected_types = serializers.ListField(child=serializers.CharField(max_length=50))
    selected_finish_types = serializers.ListField(child=serializers.CharField(max_length=50))
    selected_colors = serializers.ListField(child=serializers.CharField(max_length=50))
    all_finish_types = ProductCountSerializer(many=True)
    all_colors = ProductCountSerializer(many=True)


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


class UserLoginSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)