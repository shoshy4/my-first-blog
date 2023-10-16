from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostDraftListView, CommentFormView, PostNewView, PostEditView, \
    CommentApproveView, CommentRemoveView, PostRemoveView, PostPublishView
from django.views.generic import TemplateView


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/new/", PostNewView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('drafts/', PostDraftListView.as_view(), name='post_draft_list'),
    path('post/<pk>/publish/', PostPublishView.as_view(), name='post_publish'),
    path('post/<pk>/remove/', PostRemoveView.as_view(), name='post_remove'),
    path('post/<int:pk>/comment/', CommentFormView.as_view(), name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', CommentApproveView.as_view(), name='comment_approve'),
    path('comment/<int:pk>/remove/', CommentRemoveView.as_view(), name='comment_remove'),
]
