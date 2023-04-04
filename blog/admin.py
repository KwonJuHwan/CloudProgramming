from django.contrib import admin
from .models import Post, Category, Tag

admin.site.register(Post)


# name field 로 slug 를 자동 생성
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


# Model 과 ModelAdmin 을 묶어서 등록

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
