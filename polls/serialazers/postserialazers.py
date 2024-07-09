from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Post
from .userserializers.serialazers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    pic1 = serializers.ImageField(required=True)
    pic2 = serializers.ImageField(required=False)
    pic3 = serializers.ImageField(required=False)
    owner = UserSerializer()
    
    class Meta:
        model = Post
        fields = '__all__'

