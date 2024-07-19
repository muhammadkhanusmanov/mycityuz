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

class ListPosts(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    def get_queryset(self):
        queryset = Post.objects.all()
        branch = self.request.query_params.get('branch', None)
        if branch is not None:
            queryset = queryset.filter(branch=branch)
        return queryset

class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    def delete(self, request):
        user = request.user
        if user.last_name == 'admin':
            id = request.data.get('id', None)
            if id is not None:
                try:
                    user = User.objects.get(id=id)
                    user.delete()
                    return Response({'success': True}, status=status.HTTP_200_OK)
                except:
                    return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': False}, status=status.HTTP_403_FORBIDDEN)

class DeletePost(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    
    def delete(self,request):
        user = request.user
        post_id = request.data.get('id', None)
        if post_id is not None:
            try:
                post = Post.objects.get(id=post_id)
                print(post.owner)
                if user == post.owner or user.last_name == 'admin':
                    post.delete()
                    return Response({'success': True}, status=status.HTTP_200_OK)
                return Response({'success': False}, status=status.HTTP_403_FORBIDDEN)
            except:
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

class UserPosts(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    def post(self, request):
        user = request.user
        posts = Post.objects.filter(owner=user)
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CountView(APIView):
    def post(self, request):
        # id = request.data.get('id', None)
        # ip_address = request.META.get('REMOTE_ADDR')
        print(ip_address)
        if id is not None:
            try:
                post = Post.objects.get(id=id)
                post.views = post.views + 1
                post.save()
                return Response({'status': True}, status=status.HTTP_200_OK)
            except:
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)