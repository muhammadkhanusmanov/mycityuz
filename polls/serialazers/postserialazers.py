from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Posts
from .userserializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    pic1 = serializers.ImageField(required=True)
    pic2 = serializers.ImageField(required=False)
    pic3 = serializers.ImageField(required=False)

    class Meta:
        model = Posts
        fields = ['title', 'branch', 'position', 'description', 'location', 'pic1', 'pic2', 'pic3']

class FullPostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Posts
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Posts
        fields = ['id','title', 'branch', 'owner', 'description', 'location', 'pic1']

class PostSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id','title', 'branch', 'description', 'location', 'pic1', 'pic2', 'pic3']