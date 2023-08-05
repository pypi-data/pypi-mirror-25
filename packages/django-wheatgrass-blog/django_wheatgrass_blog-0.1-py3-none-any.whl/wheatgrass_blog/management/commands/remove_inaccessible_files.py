from django.core.management.base import BaseCommand, CommandError
from apps.article.models import Article, ArticleFile

class Command(BaseCommand):
    help = 'Removes associated article files where the article no longer exists.'

    def handle(self, *args, **options):

        # Get article files.
        # Excludes article files where the 'article' field is 0,
        # which are reserved files for non-article pages.
        files = ArticleFile.objects.exclude(article=0)

        deleted_files = 0 # The number of files deleted.
        deleted_articles = 0 # The number of articles that don't exist.

        # Delete the file if the associated article does not exist.
        for file_ in files:

            try:
                Article.objects.get(id=file_.article)
            except Article.DoesNotExist:

                deleted_file = file_

                # Delete the file
                file_.delete()

                # Log the deletion
                deleted_files += 1
                deleted_articles += 1
                self.stdout.write('Deleted file: {0}, from article {1}'.format(deleted_file.associated_file.url,
                                                                               deleted_file.article))

        self.stdout.write(self.style.SUCCESS('\nDeleted {0} files.'.format(deleted_articles)))