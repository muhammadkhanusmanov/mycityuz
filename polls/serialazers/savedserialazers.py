from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Saved
from .userserializers import UserSerializer
from ..postserialazers import PostSimpleSerializer

class SavedSerializer(serializers.ModelSerializer):
    posts = PostSimpleSerializer(many=True)
    class Meta:
        model = Saved
        fields = ['id','posts']
        
        