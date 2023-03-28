from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.

# 목록 보기 화면
class PostList(ListView):
    model = Post
    # pk의 역 순으로 나오게(최신 글이 위로 나오게)
    ordering = '-pk'


class PostDetail(DetailView):
    model = Post


def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/post_detail.html',
        {
            'post': post,
        }
    )

# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'blog/post_list.html',
#         {
#             'posts': posts,
#         }
#     )
