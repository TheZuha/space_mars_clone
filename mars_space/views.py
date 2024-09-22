from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import PostForm

@login_required
def home_page(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    is_liked = post.likes.filter(user=request.user).exists()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'form': form
    })


@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('post_detail', post_id=post_id)
