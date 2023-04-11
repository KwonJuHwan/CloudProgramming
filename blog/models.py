import os.path
from django.contrib.auth.models import User
from django.db import models


# 카테고리 만드는 것과 유사
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    # URL 에 키워드 넣기 위해서 uuid 같은 숫자가 아닌, 텍스트로 노출 가능
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    # 테스트 하기 용이
    def __str__(self):
        return self.name

    # 이름 바꿔 주기
    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    # 중복을 피하기 위해 사용 -> upload_to
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    # 자동 생성
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 관계 형성
    author = models.ForeignKey(User,null=False, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'  # 작성자 표시

    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
