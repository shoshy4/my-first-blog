from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination

from .models import Post, Comment
from .permissions import IsOwnerOrReadOnly, IsPostOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from django.utils import timezone
from django.contrib.auth import authenticate, login


class PostCreateList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    def create(self, request, *args, **kwargs):
        data = request.data
        data["owner"] = self.request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDraftList(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')


class PostUpdateDetailRemove(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostPublish(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def update(self, request, *args, **kwargs):
        data = request.data
        data["published_date"] = timezone.now()
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CommentUpdateRemoveDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentApprove(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPostOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_pk'))
    serializer_class = CommentSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        data["approved_comment"] = True
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Comment.objects.filter(post_id=self.kwargs.get('post_pk')).order_by('created_date')
        post_owner = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        if self.request.user.id != post_owner.owner_id:
            return queryset.filter(approved_comment=True)
        else:
            return queryset

    """
    def get_queryset(self):
        queryset = Comment.objects.filter(post_id=self.kwargs.get('post_pk')).order_by('created_date')
        post_owner = queryset.values_list('post_owner', flat=True)[0]
        if self.request.user.id != post_owner:
            return queryset.filter(approved_comment=True)
        else:
            return queryset
     """
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.request.data["post"])
        serializer.save(post_owner=post.owner)
