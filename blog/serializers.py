from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']


class PostSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Post 
        fields = ['id', 'title', 'content']


class CommentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Comment 
        fields = ['id', 'post', 'content']

  