import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse

# Create your tests here.

from .models import Article

class ArticleTestCase(TestCase):
    def setUp(self):
        # Create test articles
        Article.objects.create(title='Visible Article', content='Visible Article.', visible=True)
        Article.objects.create(title='Hidden Article', content='Hidden Article.', visible=False)

        # Create admin
        User.objects.create_superuser('admin', '', 'password')

    def test_article_permissions(self):
        '''Test case for article permissions.

        If the 'visible' field is True on an article, the article should be visible to all users.
        If 'visible' is false, the article should only be visible to admins.
        '''

        article_visible = reverse('article', kwargs={'id_': '1'})
        article_hidden = reverse('article', kwargs={'id_': '2'})

        # Viewing articles as a regular user
        user = Client()

        response = user.get(article_visible)
        self.assertEqual(response.status_code, 200,
                         msg='Regular users cannot see visible articles.')

        response = user.get(article_hidden)
        self.assertEqual(response.status_code, 404,
                         msg='Regular users can see hidden articles.')

        # Viewing articles as an admin
        admin = Client()
        admin.login(username='admin', password='password')

        response = admin.get(article_visible)
        self.assertEqual(response.status_code, 200,
                         msg='Admins cannot see visible articles.')

        response = admin.get(article_hidden)
        self.assertEqual(response.status_code, 200,
                         msg='Admins cannot see hidden articles.')

    def test_article_creation(self):
        '''Test case for article creation.'''

        url = reverse('api_article_create')

        user = Client()

        # Article creation by a regular user
        response = user.post(url, {
            'title': 'Title',
            'content': 'Content',
        })
        self.assertEqual(response.status_code, 403,
                         msg='Regular users can create articles.')

        # Log in as admin
        user.login(username='admin', password='password')

        # Valid article data
        response = user.post(url, {
            'title': 'Title',
            'content': 'Content',
        })
        response_json = json.loads(response._container[0].decode('utf-8'))
        self.assertEqual(response_json['submitted'], True,
                         msg='Cannot submit article with valid article data.')

        # Blank article
        response = user.post(url, {
            'title': '',
            'content': '',
        })
        response_json = json.loads(response._container[0].decode('utf-8'))
        self.assertEqual(response_json['submitted'], True,
                         msg='Cannot submit blank article.')

    def test_article_editing(self):
        '''Test case for article editing.'''

        url = reverse('api_article_edit')

        user = Client()

        # Article editing by a regular user
        response = user.post(url, {
            'id': '1',
            'title': 'Title',
            'content': 'Content',
        })
        self.assertEqual(response.status_code, 403,
                         msg='Regular users can edit articles.')

        # Log in as admin
        user.login(username='admin', password='password')

        # Valid article data
        response = user.post(url, {
            'id': '1',
            'title': 'Title',
            'content': 'Content',
        })
        response_json = json.loads(response._container[0].decode('utf-8'))
        self.assertEqual(response_json['submitted'], True,
                         msg='Cannot edit article with valid article data.')
