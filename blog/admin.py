from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'status')
    list_filter = ('author', 'status', 'publish', 'created', 'tags')
    search_fields = ('title', 'body', 'autor')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('name', 'post')
    search_fields = ('name', 'email', 'body')

admin.site.register(Post, PostAdmin)
