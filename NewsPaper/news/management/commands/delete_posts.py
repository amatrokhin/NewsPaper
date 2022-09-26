from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from news.models import Post, Category


class Command(BaseCommand):
    help = 'deletes every post in a given category'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write(f'Do you really want to delete all posts in {options["category"]}? yes/no')

        answer = input()

        if answer == 'yes':

            try:
                category = Category.objects.get(name=options['category'])
                Post.objects.filter(categories=category).delete()

                self.stdout.write(self.style.SUCCESS(f'Succesfully wiped posts from {category.name}!'))

            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category "{options["category"]}"'))

        self.stdout.write(self.style.ERROR('Access denied'))
