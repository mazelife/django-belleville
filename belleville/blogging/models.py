from datetime import datetime
from django.db import models

from settings import BloggingSettings
from managers import BloggingEntryManager

class TumblelogEntry(models.Model):
    """
    A model of a tumblelog (aka 'microblog') entry
    
    Jason Kottke describes a tumblelog as "a quick and dirty stream of 
    consciousness, a bit like a remaindered links style linklog but with more 
    than just links."
    
    """
    slug = models.SlugField(_("Slug"),
    title = models.TextField(_("Title"))
    post = models.TextField(_("Post"), blank=True)
    author = models.ForeignKey(Author, related_name="tumblelog_entries")
    status = models.CharField(_("Status"),
        max_length=1, 
        choices=BloggingSettings.PUB_STATES,
        default=BloggingSettings.DEFAULT_PUB_STATE
    )
    pub_date = models.DateTimeField(_(u"Publication Date"), 
        help_text=_("Dates in the future will not appear on the site until the \
        date is reached"),
        default=datetime.now()
    )
    post_to_twitter = models.BooleanField(_("Post to Twitter"),
        help_text=_("Post this to the account listed in your site settings.")
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
        return ("tumblelog:entry_detail", (), {'slug': self.slug})
    
    def post_to_twitter(self):
        raise NotImplementedError, "Coming soon..."
    