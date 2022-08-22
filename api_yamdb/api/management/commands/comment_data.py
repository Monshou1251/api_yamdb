from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User

LIST = {
    'User': 'users.csv',
    'Genre': 'genre.csv',
    'Category': 'category.csv',
    'Title': 'titles.csv',
    'Review': 'review.csv',
    'Comment': 'comments.csv'
}

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the Comment data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from comments.csv"

    def handle(self, *args, **options):

        # Show this if the data already exist in the database
        if Comment.objects.exists():
            print('comments data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        # Show this before loading the data into the database
        print("Loading comments data")

        # Code to load the data into database
        for models, fixture_path in LIST.items():
            for row in DictReader(open(f'{settings.BASE_DIR}/static/data/{fixture_path}', 'r', encoding='UTF-8')):
                if models == 'User':
                    user = User(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                    )
                    user.save()

                elif models == 'Genre':
                    genre = Genre(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                    genre.save()

                elif models == 'Category':
                    category = Category(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                    category.save()

                elif models == 'Title':
                    title = Title(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category=Category.objects.get(pk=row['category']),
                    )
                    title.save()

                elif models == 'Review':
                    review = Review(
                        id=row['id'],
                        title=Title.objects.get(pk=row['title_id']),
                        text=row['text'],
                        author=User.objects.get(pk=row['author']),
                        score=row['score'],
                        pub_date=row['pub_date'],
                    )
                    review.save()

                elif models == 'Comment':
                    comment = Comment(
                        id=row['id'],
                        review=Review.objects.get(pk=row['review_id']),
                        text=row['text'],
                        author=User.objects.get(pk=row['author']),
                        pub_date=row['pub_date']
                    )
                    comment.save()
        self.stdout.write(msg='Данные успешно загружены')
