from django.shortcuts import get_object_or_404, redirect, render
from .models import Comment, Post
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, identifier=post_id)
    return render(request, 'post_detail.html', {'post': post})


@login_required(login_url='network:home')
def like(request):
    post_id = request.GET['post_id']
    post = get_object_or_404(Post, identifier=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked=True
    post.save
    likes = post.likes.count()
    response = JsonResponse({'liked': liked, 'likes': likes})
    return response


@login_required(login_url='network:home')
def comment(request):
    post_id = request.GET['post_id']
    post = get_object_or_404(Post, identifier=post_id)
    comment_data = request.GET['comment']
    comment = Comment(post=post, user=request.user, body=comment_data)
    comment.save()
    response = JsonResponse({'comment': comment_data})
    return response


