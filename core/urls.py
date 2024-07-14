from django.contrib import admin
from django.urls import path
from polls.views import PostCreateView,LoginView,ListUsers,DeleteUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',LoginView.as_view()),
    path('post/add/',PostCreateView.as_view()),
    path('users/',ListUsers.as_view()),
    path('delete/user/',DeleteUser.as_view()),
]
