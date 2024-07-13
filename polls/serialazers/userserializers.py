from rest_framework.serializers import ModelSerializer, SerializerMethodField, ReadOnlyField
from django.contrib.auth.models import User
from rest_framework import serializers

class AdminSerializer(ModelSerializer):
    role = serializers.CharField(source='last_name')
    full_name = serializers.CharField(source='first_name')
    class Meta:
        model = User
        fields = ['id','username','full_name','role','email']

class UserSerializer(ModelSerializer):
    full_name = serializers.CharField(source='first_name')
    class Meta:
        model = User
        fields = ['id','username','full_name','email']
