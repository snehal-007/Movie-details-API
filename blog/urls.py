from django.urls import path
from . import views
from .views import ApiRoot ,UserList ,UserDetail ,PostDetail ,PostList

# from .views import post_list ,post_detail     # For Function Base Method

urlpatterns = [
    path('',ApiRoot.as_view(),name='root'),
    path('collect/',views.movies_collect,name="Collect"),
    path('users/',UserList.as_view(),name="users"),
    path('users/<int:pk>/',UserDetail.as_view(),name='single-user'),
    path('posts/',PostList.as_view(),name='posts'),
    path('posts/<int:pk>/',PostDetail.as_view(),name='single-post'),
]