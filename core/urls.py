from django.contrib import admin
from django.urls import path
from polls.views import (PostCreateView,LoginView,ListUsers,DeleteUser,DeletePost,
    UserPosts,ListPosts,CountView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',LoginView.as_view()),
    path('post/add/',PostCreateView.as_view()),
    path('users/',ListUsers.as_view()),
    path('delete/user/',DeleteUser.as_view()),
    path('delete/post/',DeletePost.as_view()),
    path('user/posts/',UserPosts.as_view()),
    path('list/posts/',ListPosts.as_view()),
    path('view/post/',CountView.as_view()),
]
