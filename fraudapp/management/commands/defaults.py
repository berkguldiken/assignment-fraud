import time

from django.core.management import BaseCommand
from ...default_rules import default_rules
from user.models import CustomUser
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    def handle(self, *args, **options):
        default_rules()
        if not CustomUser.objects.filter(is_superuser=True).first():
            user = CustomUser.objects.create(
                username = 'admin',
                email = 'admin@admin.com',
                is_superuser = True,
                password = make_password('admin'),
                is_staff = True,
            )
            #user.password = make_password('admin')
            user.save()
