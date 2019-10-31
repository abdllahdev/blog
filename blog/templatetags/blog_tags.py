from django import template
from django.db.models import Count
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def get_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.inclusion_tag('blog/post/most_commented_posts.html')
def get_most_commented_posts(count=5):
    most_commented_posts = Post.published.annotate(total_comments=Count('post_comments')).order_by('-total_comments')[:count]
    return {'most_commented_posts': most_commented_posts}
