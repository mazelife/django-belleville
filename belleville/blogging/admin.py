from django.contrib import admin
from django.contrib.contenttypes import generic
from django.utils.encoding import force_unicode

from models import BlogEntry, TumblelogEntry



from tagging.models import TaggedItem

class TaggingInline(generic.GenericTabularInline):
    model = TaggedItem
    extra = 3
    verbose_name_plural = "Tags for this item:"
    max_num = 10

class BlogEntryAdmin(admin.ModelAdmin):
    
    inlines = [TaggingInline]

class TumblelogEntryAdmin(admin.ModelAdmin):
    """
    An admin site object for Tumblelog entry. Handles posting to Twitter.
    """
    def save_model(self, request, obj, form, change):
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