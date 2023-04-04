from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag


# Create your views here.

# 목록 보기 화면
class PostList(ListView):
    model = Post
    # pk의 역 순으로 나오게(최신 글이 위로 나오게)
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        # getContext 에 PostList 를 담아서 넘겨 줌
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        # 미분류 개수를 받기 위해서
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        # getContext 에 PostList 를 담아서 넘겨 줌
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        # 미분류 개수를 받기 위해서
        context['no_category_count'] = Post.objects.filter(category=None).count()
        return context


# Function or IF


def categories_page(request, slug):
    if slug == 'no-category':
        category = '미분류'
        post_list = Post.objects.filter(category=None).order_by('-pk')
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category).order_by('-pk')
    # FBV  특징
    context = {
        'categories': Category.objects.all(),
        'category_less_post_count': Post.objects.filter(category=None).count(),
        'category': category,
        'post_list': post_list,
        'no_category_count': Post.objects.filter(category=None).count()
    }
    return render(request, 'blog/post_list.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all().order_by('-pk')

    # FBV  특징
    context = {
        'tag': tag,
        'post_list': post_list,
        'categories': Category.objects.all(),
        'no_category_count': Post.objects.filter(category=None).count()
    }
    return render(request, 'blog/post_list.html', context)


def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/post_detail.html',
        {
            'post': post,
        }
    )
