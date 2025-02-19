from rest_framework import serializers
from .models import APIRequest, APIResponse

class APIRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIRequest
        fields = '__all__'

class APIResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIResponse
        fields = '__all__'
