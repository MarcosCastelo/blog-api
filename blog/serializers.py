from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('street', 'suite', 'city', 'zipcode')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'post')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'body', 'profile')

class ProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = Profile
        fields = ('name', 'email', 'address')

    def create(self, validated_data):
        profile = Profile()
        profile.name = validated_data.get('name')
        profile.email = validated_data.get('email')

        address_data = validated_data.pop('address')
        address = Address()
        address.street = address_data.get('street')
        address.suite = address_data.get('suite')
        address.city = address_data.get('city')
        address.zipcode = address_data.get('zipcode')

        address.save()
        profile.address = address
        profile.save()

        return profile
        
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        address_data = validated_data.pop('address')
        address = instance.address
        address.street = address_data.get('street', address.street)
        address.suite = address_data.get('suite', address.suite)
        address.city = address_data.get('city', address.city)
        address.zipcode = address_data.get('zipcode', address.zipcode)

        address.save()
        instance.save()
        return instance


class ProfilePostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', 'posts')


class PostCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'comments')

class CommentForPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'name', 'email', 'body', 'post')


    def create(self, validated_data):
        comment = Comment()
        comment.name = validated_data.get('name')
        comment.email = validated_data.get('email')
        comment.body = validated_data.get('body')
        post = Post.objects.filter(pk=validated_data.get('post'))
        comment.post = post
        
        comment.save()

        return comment  
    
    