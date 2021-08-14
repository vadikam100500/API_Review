import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):

    MODEL_TABLE = {
        Category: 'static/data/category.csv',
        Genre: 'static/data/genre.csv',
        User: 'static/data/users.csv',
        Title: 'static/data/titles.csv',
        Review: 'static/data/review.csv',
        Comment: 'static/data/comments.csv',
        'NoModel': 'static/data/genre_title.csv'
    }

    FIELDS_WITH_ID = {
        'category': 'category_id',
        'author': 'author_id',
        'author': 'author_id'
    }

    USER_DICT = {
        'moderator': 'is_staff',
        'admin': 'is_superuser'
    }

    def handle(self, *args, **kwargs):
        for model, table in self.MODEL_TABLE.items():
            with open(table, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data = dict(row.items())
                    for key in data.keys():
                        if key in self.FIELDS_WITH_ID:
                            data[self.FIELDS_WITH_ID[key]] = data.pop(key)
                    if model is User:
                        role = data['role']
                        if role in self.USER_DICT:
                            data[self.USER_DICT[role]] = True
                    if model == 'NoModel':
                        title = Title.objects.get(id=row['title_id'])
                        genre = Genre.objects.get(id=row['genre_id'])
                        title.genre.add(genre)
                    else:
                        model(**data).save()

        self.stdout.write(self.style.SUCCESS('Your base is ready!'))
