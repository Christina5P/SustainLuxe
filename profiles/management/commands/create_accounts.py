from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import Account


class Command(BaseCommand):
    help = 'Create Account objects for existing users'

    def handle(self, *args, **options):
        users_without_account = User.objects.filter(account__isnull=True)
        created_count = 0

        for user in users_without_account:
            Account.objects.create(user=user)
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} Account objects'
            )
        )
