from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    template_name = 'post_list.html'


class PostDetailView(DetailView):
    queryset = Post.objects.all()
    template_name = 'blog/post_detail.html'
    context_object_name = "post"
    def get_object(self):
        obj = super().get_object()
        return obj



@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

class PostDraftListView(ListView):
    model = Post
    context_object_name = "posts"
    queryset = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    template_name = 'blog/post_draft_list.html'

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

class CommentFormView(View):
    form_class = CommentForm
    initial = {"key": "value"}
    template_name = "blog/add_comment_to_post.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = get_object_or_404(Post, pk=self.kwargs["pk"])
            comment.save()
            return redirect('post_detail', pk=self.kwargs["pk"])
        return render(request, self.template_name, {"form": form})
#def add_comment_to_post(request, pk):
 #   post = get_object_or_404(Post, pk=pk)
  #  if request.method == "POST":
   ##    if form.is_valid():
     #       comment = form.save(commit=False)
      #      comment.post = post
       #     comment.save()
        #    return redirect('post_detail', pk=post.pk)
    #else:
     #   form = CommentForm()
    #return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)