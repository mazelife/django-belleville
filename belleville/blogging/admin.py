from django.contrib import admin
from django.contrib.contenttypes import generic

from models import BlogEntry, TumblelogEntry



from tagging.models import TaggedItem

class TaggingInline(generic.GenericTabularInline):
    model = TaggedItem
    extra = 3
    verbose_name_plural = "Tags for this item:"
    max_num = 10

class BlogEntryAdmin(admin.ModelAdmin):
    inlines = [TaggingInline]

admin.site.register(TumblelogEntry)
admin.site.register(BlogEntry, BlogEntryAdmin)    