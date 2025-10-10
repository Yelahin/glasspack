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
