from django.contrib import admin
from .models import Tweet, Profile

class TweetAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug','hashtag', 'author')
	list_filter = ('created', 'updated')
	search_fields = ('author__username', 'title', 'hashtag')
	prepopulated_fields = {'slug': ('title',)}
	list_editable = ('author','hashtag',)
	date_hierarchy = ('created')

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'dob', 'photo')

admin.site.register(Tweet, TweetAdmin)
admin.site.register(Profile, ProfileAdmin)