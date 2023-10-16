from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostDraftListView, CommentFormView
from django.views.generic import TemplateView


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', PostDraftListView.as_view(), name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', CommentFormView.as_view(), name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
]
