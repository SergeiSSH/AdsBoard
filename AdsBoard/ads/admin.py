from django.contrib import admin
from .models import Category, Post, Comment, PostCategory


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = (PostCategoryInline,)
    list_display = ['pk', 'title', 'author', 'in_category', 'date_posted']
    list_display_links = ('pk', 'title',)
    list_filter = ('title', 'author', 'date_posted')
    search_fields = ('title', 'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'post_title', 'author', 'date_posted', 'approved']
    list_display_links = ('pk',)
    list_filter = ('post__title', 'author', 'date_posted', 'approved')
    search_fields = ('post__title', 'author')


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
