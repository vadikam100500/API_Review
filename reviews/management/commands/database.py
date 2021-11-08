import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

TABLES_DICT = {
    Category: 'static/data/category.csv',
    Genre: 'static/data/genre.csv',
    User: 'static/data/users.csv',
    Title: 'static/data/titles.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv',
    'NoModel': 'static/data/genre_title.csv'
}

USER_DICT = {
    'moderator': 'is_staff',
    'admin': 'is_superuser'
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, base in TABLES_DICT.items():
            with open(base, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                if model in (User, 'NoModel'):
                    for row in reader:
                        data = dict(row.items())
                        if model is User:
                            role = data['role']
                            if role in USER_DICT:
                                data[USER_DICT[role]] = True
                            model(**data).save()
                        if model == 'NoModel':
                            title = Title.objects.get(id=row['title_id'])
                            genre = Genre.objects.get(id=row['genre_id'])
                            title.genre.add(genre)
                else:
                    model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS('Successfully load data'))
