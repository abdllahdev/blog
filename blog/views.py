from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.conf import settings
from django.shortcuts import redirect
from haystack.query import SearchQuerySet


def post_list(request, author=None, tag_slug=None):
    """
        return a list of posts
    """ 
    posts = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = get_list_or_404(Post, tags__in=[tag])
    
    if author:
        posts = get_list_or_404(Post, author__username=author)
    
    page = request.GET.get('page')
    paginated_posts = paginate(posts, page)

    search_form = SearchForm()

    return render(request, 'blog/post/list.html', {'posts': paginated_posts,
                                                   'page': page,
                                                   'author': author,
                                                   'tag': tag,
                                                   'search_form': search_form})

def post_detail(request, year, month, day, slug):
    """
        return post details
    """
    post = get_object_or_404(Post,
                             slug=slug,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.post_comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    search_form = SearchForm()

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts,
                                                     'search_form': search_form})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        share_form = EmailPostForm(request.POST)
        if share_form.is_valid():
            cd = share_form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read {} at {}\n\n\'s comments: {}'.format(post.title, post_url, cd['comment'])
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
            return redirect('blog:post_list')
    else:
        share_form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'share_form': share_form,
                                                    'sent': sent})

def paginate(posts, page):
    """
        Paginate posts to be 5 posts in the page
    """
    p = Paginator(posts, 5)
    try:
        posts = p.page(page)
        return posts
    except PageNotAnInteger:
        posts = p.page(1)
        return posts
    except EmptyPage:
        posts = p.page(p.num_pages)
        return posts

def post_search(request):
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(content=cleaned_data['query']).load_all()
            total_results = results.count()
        return render(request, 'blog/post/list.html', {'posts': results,
                                                       'total_results': total_results,
                                                       'search_form': form})
    return render(request, 'blog/post/list.html')
