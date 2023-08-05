import imghdr

from django.http import JsonResponse, Http404
from crispy_forms.utils import render_crispy_form
from .utils.decorators import admin_required
from django.views.decorators.http import require_POST

# Create your APIs here.

from .models import Article, ArticleFile
from .forms import ArticleForm, ArticleFileForm

@admin_required
@require_POST
def create(request):
    '''The article creation API.'''

    form = ArticleForm(request.POST)

    if form.is_valid():
        article = form.save(commit=False)

        article.save()

        context = {
            'submitted': True,
            'data': {
                'id': article.id,
            },
        }
    else:
        context = {
            'submitted': False,
            'error': {
                'code': 'form_invalid',
                'form_errors': form.errors,
            },
        }

    return JsonResponse(context)

@admin_required
@require_POST
def edit(request):
    '''The article edit API.'''

    try:
        article = Article.objects.get(id=request.POST.get('id', '0'))
    except Article.DoesNotExist:
        raise Http404

    form = ArticleForm(request.POST)

    if form.is_valid():
        edit = form.save(commit=False)

        article.title = edit.title
        article.content = edit.content
        article.thumbnail = edit.thumbnail
        article.markdown = edit.markdown
        article.html = edit.html
        article.visible = edit.visible

        article.save()

        context = {
            'submitted': True,
        }
    else:
        form_html = render_crispy_form(form)
        context = {
            'submitted': False,
            'error': {
                'code': 'form_invalid',
                'form': form_html,
            },
        }

    return JsonResponse(context)

@admin_required
@require_POST
def upload_file(request):
    '''The article file uploading API.'''

    try:
        article = Article.objects.get(id=request.POST.get('article', '0'))
    except Article.DoesNotExist:
        raise Http404

    form = ArticleFileForm(request.POST, request.FILES)

    if form.is_valid():
        file_ = form.save(commit=False)

        file_.save()

        context = {
            'submitted': True,
            'data': {
                'id': file_.id,
                'file': {
                    'name': file_.associated_file.name.split('/')[-1],
                    'url': file_.associated_file.url,
                    'image': bool(imghdr.what(file_.associated_file.file.name)),
                },
            },
        }
    else:
        context = {
            'submitted': False,
            'error': {
                'code': 'form_invalid',
                'form_errors': form.errors,
            },
        }

    return JsonResponse(context)

@admin_required
@require_POST
def delete_file(request):
    '''The article file deletion API.'''

    try:
        file_ = ArticleFile.objects.get(id=request.POST.get('id', '0'))
    except ArticleFile.DoesNotExist:
        raise Http404

    # For safety, require that the POST request also specify the file path.
    # Prevents accidentally deleting the incorrect file.
    if file_.associated_file.url == request.POST.get('path', ''):
        file_.delete()
        context = {
            'submitted': True,
        }
    else:
        context = {
            'submitted': False,
            'error': {
                'code': 'incorrect_file_path',
                'message': 'The file path was incorrect.',
            },
        }

    return JsonResponse(context)
