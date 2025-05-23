from blog.models import Post, Page
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView

PER_PAGE = 9


class PostListView(ListView):
    model = Post
    template_name = "blog/pages/index.html"
    context_object_name = "posts"
    ordering = "-pk"
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"page_title": "Home - "})
        return context


def index(request):
    posts = Post.objects.get_published()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": page_obj,
            "page_title": "Home - ",
        },
    )


def created_by(request, author_pk):
    user = User.objects.filter(pk=author_pk).first()

    if user is None:
        raise Http404()

    posts = Post.objects.get_published().filter(created_by__pk=author_pk)

    user_full_name = user.username

    if user.first_name:
        user_full_name = f"{user.first_name} {user.last_name} "

    page_title = user_full_name + "posts - "

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": page_obj,
            "page_title": page_title,
        },
    )


def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()

    page_title = f"{page_obj[0].category.name} - Categoria - "

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": page_obj,
            "page_title": page_title,
        },
    )


def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()

    page_title = f"{page_obj[0].tags.first().name} - Tag - "

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": page_obj,
            "page_title": page_title,
        },
    )


def search(request):
    search_value = request.GET.get("search", "").strip()
    posts = Post.objects.get_published().filter(
        Q(title__icontains=search_value)
        | Q(excerpt__icontains=search_value)
        | Q(content__icontains=search_value)
    )[:PER_PAGE]

    page_title = f"{search_value[:20]} - Search - "

    return render(
        request,
        "blog/pages/index.html",
        {
            "page_obj": posts,
            "search_value": search_value,
            "page_title": page_title,
        },
    )


def page(request, slug):
    page_obj = get_object_or_404(
        Page.objects.get_published().filter(slug=slug),
    )

    if not page_obj:
        raise Http404()

    page_title = f"{page_obj.title} - Page - "

    return render(
        request,
        "blog/pages/page.html",
        {
            "page": page_obj,
            "page_title": page_title,
        },
    )


def post(request, slug):
    post_obj = get_object_or_404(
        Post.objects.get_published().filter(slug=slug),
    )

    if not post_obj:
        raise Http404()

    page_title = f"{post_obj.title} - Post - "

    return render(
        request,
        "blog/pages/post.html",
        {
            "post": post_obj,
            "page_title": page_title,
        },
    )
