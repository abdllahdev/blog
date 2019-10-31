from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')
    publish = indexes.DateTimeField(model_attr='publish')
    content_auto = indexes.EdgeNgramField(model_attr='body')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().published.all()
