from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required


class PostListView(ListView):
    model = Post
    paginate_by = 3
    template_name = 'post_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')



class PostDetailView(DetailView):
    queryset = Post.objects.all()
    template_name = 'blog/post_detail.html'
    context_object_name = "post"
    def get_object(self):
        obj = super().get_object()
        return obj

class PostNewView(View):
    form_class = PostForm
    initial = {"key": "value"}
    template_name = "blog/post_edit.html"

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, self.template_name, {"form": form})

class PostEditView(View):
    form_class = PostForm
    template_name = "blog/post_edit.html"

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = self.form_class(instance=post)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, self.template_name, {"form": form})

class PostDraftListView(ListView):
    model = Post
    paginate_by = 2
    context_object_name = "posts"
    queryset = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    template_name = 'blog/post_draft_list.html'

class PostPublishView(View):
    def get(self, request,pk):
        post = get_object_or_404(Post, pk=pk)
        post.publish()
        return redirect('post_detail', pk=pk)

class PostRemoveView(View):
    def get(self, request,pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('post_list')

class CommentFormView(View):
    form_class = CommentForm
    initial = {"key": "value"}
    template_name = "blog/add_comment_to_post.html"

    def get(self, request, pk):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = get_object_or_404(Post, pk=pk)
            comment.save()
            return redirect('post_detail', pk=pk)
        return render(request, self.template_name, {"form": form})

class CommentRemoveView(View):
    def get(self, request,pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)

class CommentApproveView(View):
    def get(self, request,pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.approve()
        return redirect('post_detail', pk=comment.post.pk)