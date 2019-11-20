from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import  receiver
from django.utils.text import slugify
from dateutil.relativedelta import relativedelta
from PIL import Image

class Tweet(models.Model):
	title	=	models.CharField(max_length = 100)
	slug	=	models.CharField(max_length = 120)
	author	=	models.ForeignKey(User, on_delete = models.CASCADE)
	content	=	models.TextField()
	hashtag	=	models.CharField(max_length = 100, blank=True)
	created	=	models.DateTimeField(auto_now_add = True)
	updated	=	models.DateTimeField(auto_now = True)
	likes 	=	models.ManyToManyField(User, related_name='likes', blank=True)
	class Meta:
		ordering = ['-id']

	def  __str__(self):
		return self.title

	def total_likes(self):
		return self.likes.count()

	def get_absolute_url(self):
		return reverse("tweet_detail", args=[self.id, self.slug])

@receiver(pre_save, sender=Tweet)
def pre_save_slug(sender, **kwargs):
	slug = slugify(kwargs['instance'].title)
	kwargs['instance'].slug = slug

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	dob = models.DateField(null=True, blank =True)
	photo = models.ImageField(default='deadpool.jpeg', upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.photo.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.photo.path)