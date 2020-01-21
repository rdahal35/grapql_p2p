from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# This is command for creating super user


class Command(BaseCommand):
    help = " Create custome user"

    def add_arguments(self, parser):
        self.email = input("Email: ")
        self.username = input("username: ")
        self.phone_no = input("Phone no: ")
        self.password = input("password: ")

    def handle(self, *args, **kwargs):
        user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            phone_no=self.phone_no,
            password=self.password,
            is_superuser=True,
            is_active=True,
            is_staff=True

        )
        self.stdout.write("%s user was created" % self.email)
