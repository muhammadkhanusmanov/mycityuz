from rest_framework.serializers import ModelSerializer, SerializerMethodField, ReadOnlyField
from django.contrib.auth.models import User

class AdminSerializer(ModelSerial):
    role = serializers.CharField(source='last_name')
    full_name = serializers.CharField(source='first_name')
    class Meta:
        model = User
        fields = ['id','username','full_name','role','email','created_at']

class UserSerializer(ModelSerializer):
    full_name = serializers.CharField(source='first_name')
    class Meta:
        model = User
        fields = ['id','username','full_name','email']
