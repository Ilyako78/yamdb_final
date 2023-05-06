import csv
import os

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


def add_category(row):
    Category.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def add_genre(row):
    Genre.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def add_titles(row):
    Title.objects.get_or_create(
        id=row[0],
        name=row[1],
        year=row[2],
        category_id=row[3],
    )


def add_users(row):
    User.objects.get_or_create(
        id=row[0],
        username=row[1],
        email=row[2],
        role=row[3],
        bio=row[4],
        first_name=row[5],
        last_name=row[6],
    )


def add_review(row):
    Review.objects.get_or_create(
        id=row[0],
        title_id=row[1],
        text=row[2],
        author_id=row[3],
        score=row[4],
        pub_date=row[5]
    )


def add_comment(row):
    Comment.objects.get_or_create(
        id=row[0],
        review_id=row[1],
        text=row[2],
        author_id=row[3],
        pub_date=row[4],
    )


MODEL_CSV = {
    add_category: 'category.csv',
    add_genre: 'genre.csv',
    add_titles: 'titles.csv',
    add_users: 'users.csv',
    add_review: 'review.csv',
    add_comment: 'comments.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for model, csv_f in MODEL_CSV.items():
            path = os.path.join(settings.BASE_DIR, 'static', 'data', csv_f)
            with open(path, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)

                for row in reader:
                    model(row)
            print(f'>>> Загружен файл - {csv_f}')
