from django.contrib import admin
from .models import UserProfile, BlogPosts

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(BlogPosts)


class AdminView(admin.ModelAdmin):
    list_display = ('user_profile', 'title', 'description', 'category')
