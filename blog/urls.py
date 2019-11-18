from django.urls import path, include
from blog import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('config/load-data', views.load_json),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),    
    path('profiles/', views.ProfileList.as_view(), name=views.ProfileList.name),
    path('profiles/<int:pk>', views.ProfileDetail.as_view(), name=views.ProfileDetail.name),
    path('posts/', views.PostList.as_view(), name=views.PostList.name),
    path('posts/<int:pk>', views.PostDetail.as_view(), name=views.PostDetail.name),
    path('comments/', views.CommentList.as_view(), name=views.CommentList.name),
    path('comments/<int:pk>', views.CommentDetail.as_view(), name=views.CommentDetail.name),
    path('profile-posts/', views.ProfilePostList.as_view(), name=views.ProfilePostList.name),
    path('profile-posts/<int:pk>', views.ProfilePostDetail.as_view(), name=views.ProfilePostDetail.name),
    path('post-comments/', views.PostCommentList.as_view(), name=views.PostCommentList.name),
    path('post-comments/<int:pk>', views.PostCommentDetail.as_view(), name=views.PostCommentDetail.name),
    path('posts/<int:pk>/comments', views.CommentsPostList.as_view(), name=views.CommentsPostList.name),
    path('posts/<int:post_id>/comments/<int:pk>', views.CommentsPostDetail.as_view(), name='comments-post-detail'),
    path('profile-activity', views.ProfileActivity.as_view(), name='profile-activity'),
    path('users/',views.UserList.as_view(), name=views.UserList.name),
    path('users/<int:pk>',views.UserDetail.as_view(), name=views.UserDetail.name),
    path('api-token-auth/', views.ThrottlingAuthToken.as_view(), name='token-auth')
]