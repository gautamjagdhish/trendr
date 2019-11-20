from faker import Faker
import os, django, random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from twitter.models import Tweet
from django.contrib.auth.models import User
from django.utils import timezone

def create_tweet(N):
	fake = Faker()
	for _ in range(N):
		id = random.randint(1,4)
		title = fake.name()
		Tweet.objects.create(
			title = title+"tweet!!!",
			author = User.objects.get(id=id),
			slug = "-".join(title.lower().split()),
			content = fake.text(),
			created = timezone.now(),
			updated = timezone.now(),
			)

create_tweet(10)
print("data is created successfully")