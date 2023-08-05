from django.db import models

# Create your models here.

def article_file_path(instance, filename):
    '''Returns the path of an associated article file.'''
    return 'articles/{0}/{1}'.format(instance.article, filename)

class Article(models.Model):
    '''The main model for blog posts.'''

    title = models.CharField(max_length=500, blank=True, null=False,
                             help_text='The article content.')
    content = models.CharField(max_length=500000, blank=True, null=False,
                               help_text='The article content.')
    thumbnail = models.CharField(max_length=500, blank=True, null=False,
                                 help_text='The article thumbnail image.')

    markdown = models.BooleanField(null=False, default=True,
                                   help_text='If True, Markdown formatting will be enabled.')
    html = models.BooleanField(null=False, default=True, help_text='If True, HTML will be enabled.')

    visible = models.BooleanField(null=False, default=False,
                                  help_text='If False, the article will not be publically visible.')

    time_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    time_edited = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

class ArticleFile(models.Model):
    '''The model for associated article files.'''

    associated_file = models.FileField(upload_to=article_file_path)
    article = models.CharField(max_length=50, blank=False, null=False)

    time_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    time_edited = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.associated_file.name
