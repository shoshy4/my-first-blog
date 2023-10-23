from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Post, Comment


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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.username

        return token
