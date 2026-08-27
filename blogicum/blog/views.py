from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


def published_posts():
    return Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')


def index(request):
    return render(
        request,
        'blog/index.html',
        {'post_list': published_posts()[:5]}
    )


def post_detail(request, id):
    post = get_object_or_404(published_posts(), pk=id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    current_category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = Post.objects.filter(
        category=current_category,
        pub_date__lte=timezone.now(),
        is_published=True
    ).order_by('-pub_date')
    return render(
        request,
        'blog/category.html',
        {'post_list': posts, 'category': current_category}
    )
