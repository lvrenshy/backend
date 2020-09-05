import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'

django.setup()
from user.models import Users

res = Users.objects.all()
print(res)