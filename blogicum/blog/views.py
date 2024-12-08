from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from .models import Post, Category


# Главная страница
def index(request):
    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]

    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


# Страница отдельной публикации
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)

    if post.pub_date > timezone.now():
        raise Http404("Публикация ещё не доступна.")
    if not post.is_published or not post.category.is_published:
        raise Http404("Публикация недоступна.")

    context = {'post': post}
    return render(request, 'blog/detail.html', context)


# Страница категории
def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)
