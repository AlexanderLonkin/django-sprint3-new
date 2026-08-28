from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

POSTS_COUNT = 5


def published_posts():
    """Вернуть отсортированный QuerySet доступных публикаций."""
    return Post.objects.select_related(
        'author', 'location', 'category'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    """Отобразить главную страницу с пятью последними публикациями."""
    return render(
        request,
        'blog/index.html',
        {'post_list': published_posts()[:POSTS_COUNT]}
    )


def post_detail(request, id):
    """Отобразить доступную публикацию или вернуть ошибку 404."""
    post = get_object_or_404(published_posts(), pk=id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Отобразить все доступные публикации выбранной категории."""
    current_category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = published_posts().filter(category=current_category)
    return render(
        request,
        'blog/category.html',
        {'post_list': posts, 'category': current_category}
    )
