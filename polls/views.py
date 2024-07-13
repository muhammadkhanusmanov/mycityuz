from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.http import FileResponse
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from rest_framework import generics, filters
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import F
from rest_framework.authentication import SessionAuthentication

from .serialazers.userserializers import UserSerializer,AdminSerializer
from .serialazers.postserialazers import PostSerializer,PostListSerializer
from .models import Post
from .connect import upload_image_to_dropbox


class LoginView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        rsp = AdminSerializer(user)
        token,created = Token.objects.get_or_create(user=user)
        rsp['token'] = token
        return Response(rsp,status=status.HTTP_200_OK) 


class PostCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data

            pic1_url = upload_image_to_dropbox(data['pic1'], data['pic1'].name)
            pic2_url = upload_image_to_dropbox(data['pic2'], data['pic2'].name) if data.get('pic2') else None
            pic3_url = upload_image_to_dropbox(data['pic3'], data['pic3'].name) if data.get('pic3') else None

            post = Post.objects.create(
                title=data['title'],
                branch=data['branch'],
                owner=data['owner'],
                description=data['description'],
                location=data['location'],
                pic1=pic1_url,
                pic2=pic2_url,
                pic3=pic3_url
            )

            return Response(PostListSerializer(post).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
