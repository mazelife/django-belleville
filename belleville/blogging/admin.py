from django.contrib import admin

from models import BlogEntry, TumblelogEntry

admin.site.register(TumblelogEntry)
admin.site.register(BlogEntry)
