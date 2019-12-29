import os

from django.test import TestCase

# Create your tests here.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
import django
django.setup()
from user.models import Article
print(Article.objects.all()[0].pk)