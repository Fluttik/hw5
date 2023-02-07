from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import Post, Group
from .forms import PostForm

User = get_user_model()

TOP_10 = 10  # константа для отображения количества постов


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, TOP_10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.group_posts.all()
    paginator = Paginator(post_list, TOP_10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, TOP_10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count_posts = posts.count()

    context = {
        'author': author,
        'count_posts': count_posts,
        'page_obj': page_obj
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    detail_post = get_object_or_404(Post, pk=post_id)
    post_count = detail_post.author.posts.count()
    context = {
        'detail_post': detail_post,
        'post_count': post_count
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    groups = Group.objects.all()
    context = {'groups': groups, 'form': form}
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    groups = Group.objects.all()
    form = PostForm(request.POST or None, instance=post)
    context = {'form': form, 'post': post, 'groups': groups, 'is_edit': True}
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    if form.is_valid():
        post = form.save()
        post.save()
        return redirect('posts:post_detail', post_id)
    return render(request, 'posts/post_create.html', context)
