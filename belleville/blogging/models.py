from datetime import datetime
from django.contrib.admin.models import LogEntry, ADDITION as ADD_ACTION_FLAG
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from settings import BloggingSettings
from managers import BloggingEntryManager

class TumblelogEntry(models.Model):
    """
    A model of a tumblelog (aka 'microblog') entry
    
    Jason Kottke aptly describes a tumblelog as "a quick and dirty stream of 
    consciousness, a bit like a remaindered links style linklog but with more 
    than just links."
    
    """
    slug = models.SlugField(_("Slug"))
    title = models.CharField(_("Title"), max_length=255)
    post = models.TextField(_("Post"), blank=True)
    author = models.ForeignKey('authors.Author', 
        related_name="tumblelog_entries"
    )
    status = models.CharField(_("Status"),
        max_length=25, 
        choices=BloggingSettings.PUB_STATES,
        default=BloggingSettings.DEFAULT_PUB_STATE
    )
    to_twitter = models.CharField(_("Twitter Status"),
        choices = (
            ('p', _("Post to twitter on save.")),
            ('x', _("Don't post to Twitter on save.")),
            ('d', _("Already posted to Twitter. Don't do anything on save.")),
            ('f', _("Post failed: error communicating with Twitter API ."))
        ),
        default = "x",
        help_text=_((
            "Post this to the account listed in your site settings file."
        )),
        max_length = 10
    )
    pub_date = models.DateTimeField(_(u"Publication date"), 
        help_text=_((
            "Dates in the future will not appear on the "
            "site until the date is reached"
        )),
        default=datetime.now()
    )
    
    objects = BloggingEntryManager()
    
    class Meta:
        verbose_name = "tumblelog entry"
        verbose_name_plural = 'tumblelog entries'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'    

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("tumblelog:detail", (), {'slug': self.slug})
    
    def twitter_pre_save(self, request=None):
        if self.to_twitter == 'p':
            post_sucessful = self.post_to_twitter(request=request)
            if post_sucessful:
                self.to_twitter = 'd'
                return True
            else:
                self.to_twitter = 'f'    
                return False
        return True
    
    def post_to_twitter(self, request=None):
        """
        A lightweight wrapper around http://mike.verdone.ca/twitter/ -- Mike 
        Verdone's Python Twitter Tools (PTT).
        """    
        from twitter import Twitter, TwitterError
        # If a request isn't passed, log the entry to the author:
        user_id = request and request.user.id or self.author.user.id
        max_chars = 140
        if len(self.post) > 140:
            return False 
        twitter = Twitter(
            BloggingSettings.TWITTER_EMAIL,
            BloggingSettings.TWITTER_PASSWORD
        )
        try:
            twitter.statuses.update(status=strip_tags(self.post))
            action = "Added post to %s's twitter feed." \
                % BloggingSettings.TWITTER_EMAIL
            return_status = True
        except TwitterError:
            action = (
                "Failed to post to twitter: could not connect to twitter API."
            )
            return_status = False
        # Record action in Django admin's action log:
        LogEntry.objects.log_action(
            user_id         = user_id,
            content_type_id = ContentType.objects.get_for_model(self).pk,
            object_id       = self.pk,
            object_repr     = action,
            change_message  = action,
            action_flag     = ADD_ACTION_FLAG
        )
        return return_status

class BlogEntry(models.Model):
    """A model of a blog entry"""
    pub_date = models.DateTimeField(_(u"Publication date"), 
        help_text=_((
            "Dates in the future will not appear on the "
            "site until the date is reached"
        )),
        default=datetime.now()
    )
    slug = models.SlugField(_(u"Slug"), unique_for_date='pub_date')
    headline = models.CharField(_(u"Headline"), max_length=255)
    intro = models.TextField(_(u"Intro"), help_text=_("Above the fold."))
    body = models.TextField(_(u"Body"), 
        blank=True, 
        help_text=_("Below the fold.")
    )
    author = models.ForeignKey('authors.Author', related_name="blog_entries")
    status = models.CharField(
        max_length=255, 
        choices=BloggingSettings.PUB_STATES
    )
    allow_comments = models.BooleanField(_(u"Allow comments?"), 
        default=BloggingSettings.COMMENTS_ALLOWED
    )
    objects = BloggingEntryManager()
    
    class Meta:
        verbose_name = "blog entry"
        verbose_name_plural = 'blog entries'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return "%s (%s)" % (
            self.headline, 
            self.pub_date.strftime("%h %d, %Y %H:%M %p")
        )
    
    @models.permalink
    def get_absolute_url(self):
        return ("blog:entry_detail", (), {
            'year': self.pub_date.year, 
            'month': self.pub_date.month, 
            'day': self.pub_date.day, 
            'slug': self.slug
        })
        
    @property
    def comments_enabled(self):
        if not self.allow_comments:
            return False
        delta = datetime.now() - self.pub_date
        return delta.days < BloggingSettings.DAYS_COMMENTS_OPEN
