from django.contrib import admin
from django.contrib.comments.moderation import CommentModerator, moderator
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.encoding import force_unicode
from django.contrib.comments.models import Comment

from project_utils import CKEditor

from models import BlogEntry, TumblelogEntry


from tagging.models import TaggedItem

class TaggingInline(generic.GenericTabularInline):
    model = TaggedItem
    extra = 3
    verbose_name_plural = "Tags for this item:"
    max_num = 10

class CommentsInline(generic.GenericTabularInline):
    ct_fk_field = "object_pk"
    model = Comment
    extra = 1
    verbose_name_plural = "Comments for this item:"
    max_num = 10


class BlogEntryAdmin(admin.ModelAdmin):
    """
    An admin site object for Blog entries.
    """
    date_hierarchy = 'pub_date'
    list_display = ('headline', 'pub_date', 'author', 'status')
    list_filter = ('author', 'status',)
    fieldsets = (
        (None, {
            'fields': ('slug', 'headline', 'intro', 'body')
        }),
        ('Metadata', {
            'fields': ('status', 'pub_date', 'author', 'allow_comments')
        }),
    )

    formfield_overrides = {
        models.TextField: {
            'widget' : CKEditor(ck_attrs={'height': '500px'})
        }
    }
    inlines = [TaggingInline]
    
    class Media:
        css = {"all": ("styles/admin.css",)}

class TumblelogEntryAdmin(admin.ModelAdmin):
    """
    An admin site object for Tumblelog entries. Handles posting to Twitter.
    """
    date_hierarchy = 'pub_date'
    list_display = ('title', 'pub_date', 'author', 'status')
    list_filter = ('author', 'status',)
    fieldsets = (
        (None, {
            'fields': ('slug', 'title', 'post')
        }),
        ('Metadata', {
            'fields': ('status', 'pub_date', 'author', 'to_twitter')
        }),
    )
    
    formfield_overrides = {
        models.TextField: {
            'widget' : CKEditor(ck_attrs={'height': '350px'})
        }
    }
    
    inlines = [TaggingInline]

    class Media:
        css = {"all": ("styles/admin.css",)}    
    
    def save_model(self, request, obj, form, change):
        if obj.to_twitter == 'p':
            save_successful = obj.twitter_pre_save(request=request)
            message_args = {
                'name': force_unicode(obj._meta.verbose_name),
                'obj': force_unicode(obj)
            }
            if save_successful:
                self.message_user(request, (
                    "The %(name)s \"%(obj)s\" was successfully posted to "
                    "twitter."
                ) % message_args)
            else: 
                self.message_user(request, (
                    "The %(name)s \"%(obj)s\" could not be posted to twitter. "
                    "There was an error communicating with the Twitter API."
                ) % message_args)
        super(TumblelogEntryAdmin, self).save_model(request, obj, form, change)

admin.site.register(TumblelogEntry, TumblelogEntryAdmin)
admin.site.register(BlogEntry, BlogEntryAdmin)

class BlogEntryModerator(CommentModerator):
    enable_field = 'allow_comments'

moderator.register(BlogEntry, BlogEntryModerator)