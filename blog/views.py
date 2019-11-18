from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from django import http
from .models import *
from .serializers import *
from .permissions import *
import json

def load_json(request):
    json_file = open('db.json', 'r')
    dict_json = json.load(json_file)

    for user in dict_json['users']:
        address = Address.objects.create(
            street = user['address']['street'],
            suite = user['address']['suite'],
            city = user['address']['city'],
            zipcode = user['address']['zipcode'],
        )
        profile = Profile.objects.create(
            id = user['id'],
            name = user['name'],
            email = user['email'],
            address = address
        )
    for post in dict_json['posts']:
        profile = Profile.objects.get(pk=post['userId'])
        Post.objects.create(
            id = post['id'],
            title = post['title'],
            body = post['body'],
            profile = profile
        )
    for comment in dict_json['comments']:
        post = Post.objects.get(pk=comment['postId'])
        Comment.objects.create(
            id = comment['id'],
            name=comment['name'],
            email=comment['email'],
            body=comment['body'],
            post=post
        )

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    
    def get(self, request, *args, **kwargs):
        return Response({
            'profiles' : reverse(ProfileList.name, request=request),
            'posts' : reverse(PostList.name, request=request),
            'comments' : reverse(CommentList.name, request=request),
            'profile-posts' : reverse(ProfilePostList.name, request=request),
            'post-comments' : reverse(PostCommentList.name, request=request),
            'profile-activity' : reverse('profile-activity', request=request),
            'users': reverse(UserList.name, request=request),
        })

class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-list'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-list'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name = 'comment-list'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    name = 'comment-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class ProfilePostList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfilePostSerializer
    name = 'profile-post-list'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

class ProfilePostDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfilePostSerializer
    name = 'profile-post-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class PostCommentList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCommentSerializer
    name = 'post-comment-list'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class PostCommentDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCommentSerializer
    name = 'post-comment-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class CommentsPostList(generics.ListCreateAPIView):
    serializer_class = CommentForPostSerializer
    name = 'comments-post-list'        

    def get_queryset(self):
        pk = self.kwargs['pk']
        post = Post.objects.filter(pk=pk)[0]
        return post.comments


class CommentsPostDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    def get_queryset(self, post_id, pk):
        try:
            post = Comment.objects.filter(post_id=post_id)
            return post[pk-1]
        except Comment.DoesNotExist:
            raise http.Http404
    

    def get(self, request, post_id, pk):
        comment = self.get_queryset(post_id, pk)
        comment_serialized = CommentForPostSerializer(comment)
        return Response(comment_serialized.data, status=status.HTTP_200_OK)

    
    def put(self, request, post_id, pk):
        comment = self.get_queryset(post_id, pk)
        request.data['post_id'] = post_id
        comment_serialized = CommentForPostSerializer(comment, data=request.data)
        if comment_serialized.is_valid():
            comment_serialized.save()
            return Response(comment_serialized.data, status=status.HTTP_200_OK)
        return Response(comment_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, pk):
        comment = self.get_queryset(post_id, pk)
        comment.delete()
        return Response(status=status.HTTP_200_OK)


class ProfileActivity(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        activity = []
        for profile in profiles:
            data = {}
            data['id'] = profile.pk
            data['name'] = profile.name
            posts = Post.objects.filter(profile_id=profile.pk)
            data['total_posts'] = len(posts)
            comments = Comment.objects.filter(email=profile.email)
            data['total_comments'] = len(comments)
            activity.append(data)
        return Response(activity, status=status.HTTP_200_OK)

     
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'