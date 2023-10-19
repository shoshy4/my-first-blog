from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['author', 'owner', 'title', 'text', 'created_date', 'published_date']


class CommentSerializer(serializers.ModelSerializer):
    post_owner = serializers.ReadOnlyField(source='post_owner.username')

    class Meta:
        model = Comment
        fields = ['post', 'author', 'text', 'created_date', 'approved_comment', 'post_owner']
