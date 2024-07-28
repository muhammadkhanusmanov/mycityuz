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
from .serialazers.postserialazers import PostSerializer,PostListSerializer,PostSimpleSerializer,FullPostSerializer
from .serialazers.savedserialazers import SavedSerializer
from .models import Posts,Saved
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

# class SignUp(APIView):
#     def post(self, request, *args, **kwargs):


class PostCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            pic1_url = upload_image_to_dropbox(data['pic1'], data['pic1'].name)
            pic2_url = upload_image_to_dropbox(data['pic2'], data['pic2'].name) if data.get('pic2') else None
            pic3_url = upload_image_to_dropbox(data['pic3'], data['pic3'].name) if data.get('pic3') else None

            post = Posts.objects.create(
                title=data['title'],
                branch=data['branch'],
                position = data['position'],
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
    queryset = Posts.objects.all()
    serializer_class = PostSimpleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    def get_queryset(self):
        queryset = Posts.objects.all()
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

class CountView(APIView):
    def post(self, request):
        id = request.data.get('id', None)
        # ip_address = request.META.get('REMOTE_ADDR')
        if id is not None:
            try:
                post = Posts.objects.get(id=id)
                post.views = post.views + 1
                post.save()
                return Response({'status': True}, status=status.HTTP_200_OK)
            except:
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


from social_django.utils import psa
from social_django.utils import load_strategy, load_backend
from social_core.actions import do_complete
from social_core.backends.utils import get_backend
from social_core.exceptions import AuthAlreadyAssociated
from django.contrib.auth import get_user_model
from social_core.exceptions import AuthForbidden, AuthAlreadyAssociated

User = get_user_model()

class GoogleLogin(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('access_token')

        if not token:
            return Response({'error': 'Missing access token'}, status=status.HTTP_400_BAD_REQUEST)

        strategy = load_strategy(request)
        backend = load_backend(strategy, 'google-oauth2', redirect_uri=None)

        try:
            user = backend.do_auth(token, ajax=True, *args, **kwargs)
            if user and user.is_active and User.objects.filter(email=user.email).exists():
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'User does not exist or authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
        except AuthAlreadyAssociated:
            return Response({'error': 'This account is already in use'}, status=status.HTTP_400_BAD_REQUEST)
        except AuthForbidden:
            return Response({'error': 'Your credentials aren\'t allowed'}, status=status.HTTP_403_FORBIDDEN)

class GoogleRegister(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('access_token')

        if token is None:
            return Response({'error': 'Missing access token'}, status=status.HTTP_400_BAD_REQUEST)

        strategy = load_strategy(request)
        backend = load_backend(strategy, 'google-oauth2', redirect_uri=None)

        try:
            user = backend.do_auth(token, ajax=True, *args, **kwargs)
            if user and user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
        except AuthAlreadyAssociated:
            return Response({'error': 'This account is already in use'}, status=status.HTTP_400_BAD_REQUEST)
        except AuthForbidden:
            return Response({'error': 'Your credentials aren\'t allowed'}, status=status.HTTP_403_FORBIDDEN)

class ChangeProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        user = request.user
        username = request.POST.get('username', user.username)
        full_name = request.POST.get('full_name', user.first_name)
        phone_number = request.POST.get('phone_number', user.last_name.split('/')[1])

        user.username = username
        user.first_name = full_name
        user.last_name = phone_number
        try:
            user.save()

            return Response({'success': True}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Failed to update profile'}, status=status.HTTP_400_BAD_REQUEST)
    
# user get own profile     
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self,request):
        user = request.user
        ser_user = UserSerializer(user)
        posts = Posts.objects.filter(user=user)
        posts = PostSimpleSerializer(posts)
        data = {"owner":ser_user.data,"posts":posts.data}
        return Response(data,status=status.HTTP_200_OK)


# get a post
class GetPost(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request):
        id = data.get('id',None)
        if id is not None:
            try:
                post = Posts.objects.get(id=id)
                ser_post = FullPostSerializer(post)
                return Response(ser_post.data,status=status.HTTP_200_OK)
            except:
                return Response({'status':False,'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status':False,'error': 'Missing id'}, status=status.HTTP_400_BAD_REQUEST)


# saved post
class SavePost(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request):
        user = request.user
        post_id = data.get('id',None)
        try:
            saved = Saved.objects.get(user=user)
            if post_id is not None:
                post = Posts.objects.get(id=post_id)
                saved.posts.add(post)
                saved.save()
                return Response({'status':True,'message': 'Post saved successfully'}, status=status.HTTP_200_OK)
            return Response({'status':False,'message': 'Not found post'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            saved = Saved.objects.create(user=user)
            saved.posts.add(post)
            saved.save()
            return Response({'status':True,'message': 'Post saved successfully'}, status=status.HTTP_200_OK)