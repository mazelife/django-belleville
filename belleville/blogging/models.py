from datetime import datetime
from django.db import models
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
    title = models.TextField(_("Title"))
    post = models.TextField(_("Post"), blank=True)
    author = models.ForeignKey('authors.Author', 
        related_name="tumblelog_entries"
    )
    status = models.CharField(_("Status"),
        max_length=25, 
        choices=BloggingSettings.PUB_STATES,
        default=BloggingSettings.DEFAULT_PUB_STATE
    )
    to_twitter = models.BooleanField(_("Post to Twitter"),
        help_text=_("Post this to the account listed in your site settings file.")
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
    
    def post_to_twitter(self):
        raise NotImplementedError, "Coming soon..."

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
        delta = datetime.datetime.now() - self.pub_date
        return delta.days < BlogSettings.DAYS_COMMENTS_OPEN  