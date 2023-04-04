import os.path
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    # URL 에 키워드 넣기 위해서 uuid 같은 숫자가 아닌, 텍스트로 노출 가능
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self): # 테스트 하기 용이
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 같이 삭제
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'  # 작성자 표시

    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
