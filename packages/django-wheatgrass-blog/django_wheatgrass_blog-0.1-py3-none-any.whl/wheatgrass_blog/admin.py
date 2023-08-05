from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

from .models import Article, ArticleFile
from .forms import ArticleForm, ArticleFileForm

class ArticleResource(resources.ModelResource):
    '''The model resource for the Article model.'''

    class Meta:
        model = Article

class ArticleFileResource(resources.ModelResource):
    '''The model resource for the ArticleFile model.'''

    class Meta:
        model = ArticleFile

class ArticleAdmin(ImportExportModelAdmin):
    '''The admin page for the Article model.'''

    resource_class = ArticleResource

    list_display = [
        'title',
        'time_created',
        'time_edited',
        'visible',
    ]

    form = ArticleForm

class ArticleFileAdmin(ImportExportModelAdmin):
    '''The admin page for the ArticleFile model.'''

    resource_class = ArticleFileResource

    list_display = [
        'article',
        'associated_file',
    ]

    form = ArticleFileForm

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleFile, ArticleFileAdmin)
