from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.http import FileResponse
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import F
from rest_framework.authentication import SessionAuthentication

from .serialazers.userserializers import UserSerializer,AdminSerializer


class LoginView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        rsp = AdminSerializer(user)
        token,created = Token.objects.get_or_create(user=user)
        rsp['token'] = token
        return Response(rsp,status=status.HTTP_200_OK) 