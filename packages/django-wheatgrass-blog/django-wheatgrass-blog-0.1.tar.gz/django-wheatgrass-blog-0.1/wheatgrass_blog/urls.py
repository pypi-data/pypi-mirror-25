'''django-wheatgrass-blog URL Configuration'''

from django.conf.urls import url

from . import views
from . import api

# Regular webpages
pages = [

    # Articles
    url(r'^articles/$', views.list_, name='article_list'),
    url(r'^articles/create/$', views.create, name='article_create'),
    url(r'^articles/a/(?P<id_>[0-9]+)/$', views.article, name='article'),
    url(r'^articles/edit/(?P<id_>[0-9]+)/$', views.edit, name='article_edit'),

]

# API pages
apis = [

    # Articles
    url(r'^api/articles/create/$', api.create, name='api_article_create'),
    url(r'^api/articles/edit/$', api.edit, name='api_article_edit'),

    # Article files
    url(r'^api/articles/file/upload/$', api.upload_file, name='api_article_file_upload'),
    url(r'^api/articles/file/delete/$', api.delete_file, name='api_article_file_delete'),
]

# Create the 'urlpatterns' list from 'pages' and 'apis'.
urlpatterns = pages + apis
