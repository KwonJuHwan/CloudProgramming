from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import CommentForm
from .models import Post, Category, Tag


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image',
              'file_upload', 'category', 'tag']
    # like FBV, template 강제 할당
    template_name = "blog/post_update.html"

    # 권한 확인
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.get_object().author == request.user:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError


# LoginRequiredMixin 로그 아웃 상태 -> accounts/login url 로 이동 시킴
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'head_image',
              'file_upload', 'category', 'tag']

    # 권한 체크
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    # form 정보를 user 가 보냈을 떄(request.user 로 받을 수 있음), 검증 실행
    def form_valid(self, form):
        # 로그인이 되어있다면
        if self.request.user.is_authenticated \
                and (self.request.user.is_staff or self.request.user.is_superuser):
            form.instance.author = self.request.user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

    def get_context_data(self, *, object_list=None, **kwargs):
        # getContext 에 PostList 를 담아서 넘겨 줌
        context = super(PostCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        # 미분류 개수를 받기 위해서
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


# 목록 보기 화면
class PostList(ListView):
    model = Post
    # pk의 역 순으로 나오게(최신 글이 위로 나오게)
    ordering = '-pk'

    # CBC 특징 get_context_data 오버라이딩한 후 ,
    # context에 원하는 데이터 보내주기
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
        # 댓글 폼 넘기기
        context['comment_form'] = CommentForm
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


def add_comment(request, pk):
    if request.user.is_authenticated:
        raise PermissionError

    # pk를 통해, Post 찾기 for Redirect
    if request.method == 'POST':
        # 존재 하지 않는 글에 댓글 접근 하는 경우를 만들어줘야함 (동시성)
        post = Post.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        # DB 에 넣기 전 필요한 field 를 채우기 위해 temp 생성
        comment_temp = comment_form.save(commit=False)
        comment_temp.post = post
        comment_temp.author = request.user
        # DB 에 넣기
        comment_temp.save()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionError
