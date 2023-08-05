from django.core.management.base import BaseCommand, CommandError
from apps.article.models import Article, ArticleFile

class Command(BaseCommand):
    help = 'Removes blank articles with no title, content, thumbnail or associated files.'

    def handle(self, *args, **options):

        # Get all articles with no title, content or thumbnail.
        articles = Article.objects.filter(title='', content='', thumbnail='')

        deleted_articles = 0

        # Delete the article if it does not have any associated files.
        for article in articles:
            if ArticleFile.objects.filter(article=article.id).count() == 0:

                deleted_article = article.id

                # Delete the article
                article.delete()

                # Log the deletion
                deleted_articles += 1
                self.stdout.write('Deleted article: {0}'.format(deleted_article))

        self.stdout.write(self.style.SUCCESS('\nDeleted {0} articles.'.format(deleted_articles)))
