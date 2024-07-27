from django.contrib import admin
from django.urls import path,include
from polls.views import (PostCreateView,LoginView,ListUsers,DeleteUser,DeletePost,
    UserProfile,ListPosts,CountView,GoogleLogin,GoogleRegister,ChangeProfile,
    GetPost)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('login/',LoginView.as_view()),
    path('post/add/',PostCreateView.as_view()),
    path('users/',ListUsers.as_view()),
    path('delete/user/',DeleteUser.as_view()),
    path('delete/post/',DeletePost.as_view()),
    path('user/posts/',UserProfile.as_view()),
    path('list/posts/',ListPosts.as_view()),
    path('view/post/',CountView.as_view()),
    path('google/login/',GoogleLogin.as_view()),
    path('google/register/',GoogleRegister.as_view()),
    path('edit/profile/',ChangeProfile.as_view()),
    path('get/post/', GetPost.as_view())
]
