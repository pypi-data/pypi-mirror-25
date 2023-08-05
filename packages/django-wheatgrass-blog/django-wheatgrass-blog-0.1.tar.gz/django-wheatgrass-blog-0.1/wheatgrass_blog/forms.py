from django import forms

from .models import Article, ArticleFile

class ArticleForm(forms.ModelForm):
    '''The form for the Article model.'''

    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'thumbnail',
            'markdown',
            'html',
            'visible',
        ]
        widgets = {
            'content': forms.Textarea(attrs={
                'cols': 125,
                'rows': 40,
            }),
        }

class ArticleFileForm(forms.ModelForm):
    '''The form for the ArticleFile model.'''

    class Meta:
        model = ArticleFile
        fields = [
            'associated_file',
            'article',
        ]
