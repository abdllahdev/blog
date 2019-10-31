from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import PostSitemap

app_name = 'blog'

sitemaps = {
    'posts': PostSitemap
}

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        views.post_detail, name='post_detail'),
    url(r'^author/(?P<author>\w+)/$', views.post_list, name='post_by_author'),
    url(r'^share/(?P<post_id>\d+)/$', views.post_share, name='post_share'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_by_tag'),
    url(r'^search/$', views.post_search, name='post_search'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
