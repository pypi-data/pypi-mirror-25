import imghdr

from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from .utils.functions import parse_formatting, surrounding_pages
from .utils.decorators import admin_required

# Create your views here.

from .models import Article, ArticleFile
from .forms import ArticleForm

def list_(request):
    '''The article list page.'''

    if request.user.is_staff:
        articles_query = Article.objects.order_by('-time_created')
    else:
        articles_query = Article.objects.filter(visible=True).order_by('-time_created')

    # Pagination
    paginator = Paginator(articles_query, 10)
    page = request.GET.get('page', 1)

    try:
        articles = paginator.page(page)
    except EmptyPage:
        # Return the last page with content
        articles = paginator.page(paginator.num_pages)

    context = {
        'articles': articles,
        'pagination': {
            'surrounding': surrounding_pages(paginator, page),
        },
        'navbar': {
            'selected': 'articles',
        },
    }

    return render(request, 'wheatgrass_blog/article-list.html', context)

def article(request, id_):
    '''The article page.'''

    try:
        if request.user.is_staff:
            article = Article.objects.get(id=id_)
        else:
            article = Article.objects.get(id=id_, visible=True)
    except Article.DoesNotExist:
        raise Http404

    # Parses formatting
    article.content = parse_formatting(article.content, html=article.html,
                                       markdown=article.markdown)

    context = {
        'article': article,
        'navbar': {
            'selected': 'articles',
        },
    }

    return render(request, 'wheatgrass_blog/article.html', context)

@admin_required
def create(request):
    '''The article creation page.'''

    context = {
        'no_redirect': bool(request.GET.get('no_redirect', '')),
    }

    return render(request, 'wheatgrass_blog/article-create.html', context)

@admin_required
def edit(request, id_):
    '''The article edit page.'''

    try:
        article = Article.objects.get(id=id_)
    except Article.DoesNotExist:
        raise Http404

    article_data = {
        'title': article.title,
        'content': article.content,
        'thumbnail': article.thumbnail,
        'markdown': article.markdown,
        'html': article.html,
        'visible': article.visible,
    }

    form = ArticleForm(article_data)

    # Associated article files
    files = ArticleFile.objects.filter(article=article.id).order_by("-time_created")


    filenames = []
    file_is_image = []
    for file_ in files:
        # Get the filename of each file
        filenames.append(file_.associated_file.name.split('/')[-1])

        # Check if each file is an image
        file_is_image.append(bool(imghdr.what(file_.associated_file.file.name)))

    article_files = zip(files, filenames, file_is_image)

    context = {
        'template': {
            'container_default': True,
        },

        'article': article,
        'article_files': article_files,
        'form': form,
        'edit': True,
    }

    return render(request, 'wheatgrass_blog/article-edit.html', context)
